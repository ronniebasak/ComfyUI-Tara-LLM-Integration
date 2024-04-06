import openai
import orjson
import os.path
import os


# GROQ_API_KEY = "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"

SERVICE_TO_KEY_FIELD = {
    "openai": "OPENAI_API_KEY",
    "groq": "GROQ_API_KEY",
    "together": "TOGETHER_API_KEY",
    # Add more services here as needed
}

FILE_NAME = "API_KEYS.json"

MODEL_DICT = {
    "openai": ["gpt-3.5turbo", "gpt-4-turbo-preview"],
    "groq": ["llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"],
    "together": ["coming-soon"],
}

BASE_LLM_CONFIG = {
    "temperature": 0.4,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0.3,
    "response_format": {"type": "json_object"},
    "presence_penalty": 0,
    "stream": False,
    "timeout": 60,
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


class GroqMaster:
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
    CATEGORY = "llm"

    def configure_chat_creation(self, provider, api_key, model, messages, overrides):
        config = {
            **BASE_LLM_CONFIG,
            **overrides,
        }
        config["stream"] = False

        print("proivder", provider)

        if provider == "groq":
            oai = openai.OpenAI(
                base_url="https://api.groq.com/openai/v1", api_key=api_key
            )
            response = oai.chat.completions.create(
                model=model,
                messages=messages,
                **config,
            )

        elif provider == "openai":
            oai = openai.OpenAI(api_key=api_key)
            response = oai.chat.completions.create(
                model=model,
                messages=messages,
                **config,
            )
        # Add more providers as needed
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        data = orjson.loads(response.choices[0].message.content)
        return data

    def generate_prompt(
        self, api_key, model, guidance, prompt_positive, prompt_negative
    ):

        msgs = [
            {
                "role": "system",
                "content": META_PROMPT,
            },
            {
                "role": "user",
                "content": f"""Guidance: {guidance}\n\nPositive Prompt: {prompt_positive}\n\nNegative Prompt: {prompt_negative}""",
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

        data = self.configure_chat_creation(provider, api_key, model_name, msgs, overrides)

        print(data)
        return data["positive"], data["negative"]


class GroqAPIKeyLoader:        
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("api_key",)
    FUNCTION = "load_api_key"
    CATEGORY = "llm"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "provider": (
                    [
                        "groq",
                        "openai",
                        "together",
                        # Add more services here as needed
                    ],
                ),
                "temporary": ("BOOLEAN", {"default": False}),
            }
        }


    # Rest of the class remains the same...

    def load_api_key(self, provider, temporary):
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


class GroqAPIKeySaver:
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
