import openai
import orjson
import os.path
import os


SERVICE_TO_KEY_FIELD = {
    "openai": "OPENAI_API_KEY",
    "groq": "GROQ_API_KEY",
    "together": "TOGETHER_API_KEY",
    # Add more services here as needed
}

FILE_NAME = "API_KEYS.json"

MODEL_DICT = {
    "openai": ["gpt-3.5-turbo", "gpt-4-turbo-preview"],
    "groq": ["llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"],
    "together": ["coming-soon"],
}

BASE_LLM_CONFIG = {
    "MAIN": {
        "temperature": 0.4,
        "max_tokens": 1000,
        "top_p": 1,
        "frequency_penalty": 0,
        "response_format": {"type": "json_object"},
        "presence_penalty": 0,
        "stream": False,
        "timeout": 60,
    },
    "DAISY_CHAIN": {
        "temperature": 0.4,
        "max_tokens": 1000,
        "top_p": 1,
        "frequency_penalty": 0.3,
        "presence_penalty": 0,
        "stream": False,
        "timeout": 60,
    },
}

META_PROMPT = """Use a JSON format for the output in the below format
{"positive": "<positive prompt as string>", "negative": "<negative prompt as string>"}
"""


def get_model_names(model_dict):
    model_list = []
    for provider, models in model_dict.items():
        for model in models:
            model_list.append(f"{provider}/{model}")
    return model_list


def get_llm_config(variant="MAIN", overrides={}):
    return {
        **BASE_LLM_CONFIG[variant],
        **overrides,
    }


def get_openai(provider, api_key):
    if provider == "groq":
        return openai.OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
    elif provider == "openai":
        return openai.OpenAI(api_key=api_key)
    # Add more providers as needed
    else:
        raise ValueError(f"Unsupported provider: {provider}")


class TaraPrompter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
                "model": (get_model_names(MODEL_DICT),),
                "guidance": ("STRING", {"multiline": True}),
                "prompt_positive": ("STRING", {"multiline": True}),
                "prompt_negative": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "generate_prompt"
    CATEGORY = "tara-llm"

    def configure_chat_creation(self, provider, api_key, model, messages, overrides):
        config = get_llm_config()
        config["stream"] = False

        oai = get_openai(provider, api_key)
        response = oai.chat.completions.create(
            model=model,
            messages=messages,
            **config,
        )

        data = orjson.loads(response.choices[0].message.content)
        return data

    def post_process_prompt(self, prompt):
        prompt = prompt.replace("{", "").replace("}", "")
        # Replace colon and comma (JSON-esque formatting)
        prompt = prompt.replace(":", "").replace(",", "")
        # Remove all quotes
        prompt = prompt.replace('"', "").replace("'", "")
        # Strip whitespaces
        prompt = prompt.strip()

        return prompt

    def generate_prompt(
        self, api_key, model, guidance, prompt_positive, prompt_negative
    ):

        msgs = [
            {
                "role": "system",
                "content": f"""{META_PROMPT}\n\nUse the below guidance and prompts to generate a positive and negative prompt. The positive prompt describes features we want, and the negative describes things we don't want.\n\nGuidelines: {guidance}""",
            },
            {
                "role": "user",
                "content": f"""Provided Positive Prompt: {prompt_positive}\n\nProvided Negative Prompt: {prompt_negative}""",
            },
        ]

        overrides = {
            "temperature": 0.4,
            "max_tokens": 1000,
            "top_p": 1,
            "frequency_penalty": 0.3,
            "response_format": {"type": "json_object"},
            "presence_penalty": 0,
            "stream": False,
            "timeout": 60,
        }

        provider, model_name = tuple(model.split("/")[:2])
        print("Data", model, provider, api_key, msgs, overrides)

        data = self.configure_chat_creation(
            provider, api_key, model_name, msgs, overrides
        )

        print(data)
        return self.post_process_prompt(data["positive"]), self.post_process_prompt(data["negative"])


class TaraAPIKeyLoader:
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("api_key",)
    FUNCTION = "load_api_key"
    CATEGORY = "tara-llm"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (get_model_names(MODEL_DICT), {"forceInput": True}),
                "temporary": ("BOOLEAN", {"default": False}),
            }
        }

    # Rest of the class remains the same...

    def load_api_key(self, model, temporary):
        provider = model.split("/")[0]
        base = os.path.dirname(__file__)
        if temporary:
            base = "/tmp"

        try:
            with open(os.path.join(base, FILE_NAME), "r") as f:
                data = orjson.loads(f.read())
                key_field = SERVICE_TO_KEY_FIELD[provider]
                return (data[key_field],)
        except FileNotFoundError:
            raise FileNotFoundError(f"API key not found in {FILE_NAME}")


class TaraAPIKeySaver:
    RETURN_TYPES = ()
    FUNCTION = "save_api_key"
    CATEGORY = "llm"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "provider": (
                    [
                        "groq",
                        "openai",
                        "together",
                    ],
                ),
                "api_key": ("STRING", {"multiline": False, "default": ""}),
                "temporary": ("BOOLEAN", {"default": False}),
            }
        }

    # Rest of the class remains the same...

    def save_api_key(self, provider, api_key, temporary):
        base = os.path.dirname(__file__)
        if temporary:
            base = "/tmp"

        key_field = SERVICE_TO_KEY_FIELD[provider]

        dat = {}

        if os.path.exists(os.path.join(base, FILE_NAME)):
            with open(os.path.join(base, FILE_NAME), "r") as f:
                dat = orjson.loads(f.read())

        with open(os.path.join(base, FILE_NAME), "w") as f:
            dat[key_field] = api_key
            f.write(orjson.dumps(dat).decode("utf-8"))

        return ()


class TaraDaisyChainNode:
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_text",)
    FUNCTION = "generate_text"
    CATEGORY = "tara-llm"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False, "forceInput": True}),
                "model": (get_model_names(MODEL_DICT), {"forceInput": True}),
                "temperature": ("FLOAT", {"default": 0.4}),
                "max_tokens": ("INT", {"default": 1000}),
                "top_p": ("FLOAT", {"default": 1}),
                "frequency_penalty": ("FLOAT", {"default": 0}),
                "presence_penalty": ("FLOAT", {"default": 0}),
                "guidance": ("STRING", {"multiline": True}),
            },
            "optional": {
                "prompt": ("STRING", {"multiline": True, "forceInput": True}),
                "positive": ("STRING", {"multiline": True, "forceInput": True}),
                "negative": ("STRING", {"multiline": True, "forceInput": True}),
            },
        }

    def configure_chat_creation(self, provider, api_key, model, messages, overrides):
        config = get_llm_config("DAISY_CHAIN", overrides=overrides)
        config["stream"] = False

        oai = get_openai(provider, api_key)
        response = oai.chat.completions.create(
            model=model,
            messages=messages,
            **config,
        )

        return response.choices[0].message.content

    def generate_text(
        self,
        api_key,
        model,
        guidance,
        temperature,
        max_tokens,
        top_p,
        frequency_penalty,
        presence_penalty,
        prompt="",
        positive="",
        negative="",
    ):
        print("DEBUG INPUT DC GUIDANCE:::", guidance)
        print("DEBUG INPUT DC PROMPT:::", prompt)
        print("DEBUG INPUT DC POSITIVE:::", positive)
        print("DEBUG INPUT DC NEGATIVE:::", negative)

        provider, model_name = tuple(model.split("/")[:2])

        overrides = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }

        msgs = [
            {
                "role": "system",
                "content": guidance,
            },
            {
                "role": "user",
                "content": f"""Provided Prompt: {prompt}""",
            },
        ]

        if positive:
            msgs.append(
                {
                    "role": "user",
                    "content": f"""Positive: {positive}""",
                }
            )

        if negative:
            msgs.append(
                {
                    "role": "user",
                    "content": f"""Negative: {negative}""",
                }
            )

        response = self.configure_chat_creation(
            provider, api_key, model_name, msgs, overrides
        )

        print("DEBUG RESPONSE::::: ", response)

        return (response,)
