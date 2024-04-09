import openai
import orjson
import os.path
import os
from .tara_llm_config import TaraLLMConfig
from .tara_master import (
    get_llm_config,
    META_PROMPT,
    post_process_prompt,
    get_model_names,
    MODEL_DICT,
    TaraAPIKeyLoader,
)


class TaraPrompterAdvancedNode:
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "generate_prompt"
    CATEGORY = "tara-llm"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "llm_config": ("TARA_LLM_CONFIG", {"forceInput": True}),
                "guidance": ("STRING", {"multiline": True}),
                "prompt_positive": ("STRING", {"multiline": True}),
            },
            "optional": {
                "prompt_negative": ("STRING", {"multiline": True}),
            },
        }

    @staticmethod
    def configure_chat_creation(llm_config, messages, overrides):
        config = get_llm_config(overrides=overrides)
        config["stream"] = False

        oai = openai.OpenAI(
            base_url=llm_config.base_url,
            api_key=llm_config.api_key,
        )

        response = oai.chat.completions.create(
            model=llm_config.llm_model,
            messages=messages,
            **config,
        )

        data = orjson.loads(response.choices[0].message.content)
        return data

    def generate_prompt(
        self,
        llm_config,
        guidance,
        prompt_positive,
        prompt_negative="",
    ):

        msgs = [
            {
                "role": "system",
                "content": f"""{META_PROMPT}\n\nUse the below guidance and appropriate prompts to generate a positive {"and negative" if prompt_negative else ""} prompt. The positive prompt describes features we want, and the negative describes things we don't want.\n\nGuidelines: {guidance}""",
            },
            {
                "role": "user",
                "content": f"""Provided Positive Prompt: {prompt_positive}{f"\n\nProvided Negative Prompt: {prompt_negative}" if  prompt_negative else ""}""",
            },
        ]

        overrides = {
            "temperature": llm_config.temperature,
            "max_tokens": llm_config.max_tokens,
            "top_p": llm_config.top_p,
            "frequency_penalty": llm_config.frequency_penalty,
            "presence_penalty": llm_config.presence_penalty,
            "response_format": {"type": "json_object"},
            "seed": llm_config.seed,
            "stream": False,
            "timeout": llm_config.timeout,
        }

        data = self.configure_chat_creation(llm_config, msgs, overrides)

        return post_process_prompt(data["positive"]), post_process_prompt(
            data["negative"]
        )


class TaraAdvancedCompositionNode:
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_text",)
    FUNCTION = "generate_text"
    CATEGORY = "tara-llm"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "llm_config": ("TARA_LLM_CONFIG", {"forceInput": True}),
                "guidance": ("STRING", {"multiline": True}),
            },
            "optional": {
                "prompt": ("STRING", {"multiline": True, "forceInput": True}),
                "positive": ("STRING", {"multiline": True, "forceInput": True}),
                "negative": ("STRING", {"multiline": True, "forceInput": True}),
            },
        }

    def generate_prompt(
        self,
        llm_config,
        guidance,
        prompt="",
        positive="",
        negative="",
    ):
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
                    "content": f"Positive: {positive}",
                }
            )

        if negative:
            msgs.append(
                {
                    "role": "user",
                    "content": f"Negative: {negative}",
                }
            )

        overrides = {
            "temperature": llm_config.temperature,
            "max_tokens": llm_config.max_tokens,
            "top_p": llm_config.top_p,
            "frequency_penalty": llm_config.frequency_penalty,
            "presence_penalty": llm_config.presence_penalty,
            "response_format": {"type": "json_object"},
            "seed": llm_config.seed,
            "stream": False,
            "timeout": llm_config.timeout,
        }

        data = TaraPrompterAdvancedNode.configure_chat_creation(
            llm_config, msgs, overrides
        )

        return post_process_prompt(data["positive"]), post_process_prompt(
            data["negative"]
        )


class TaraLLMConfigNode:
    RETURN_TYPES = ("TARA_LLM_CONFIG",)
    RETURN_NAMES = ("llm_config",)
    FUNCTION = "get_llm_config"
    CATEGORY = "tara-llm"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_url": ("STRING", {"default": "http://localhost:11434/v1"}),
                "api_key": ("STRING", {"multiline": False, "default": ""}),
                "llm_model": ("STRING", {"default": "mixtral"}),
                "temperature": ("FLOAT", {"default": 0.4}),
                "seed": ("INT", {"default": 42}),
                "max_tokens": ("INT", {"default": 1000}),
                "top_p": ("FLOAT", {"default": 1}),
                "frequency_penalty": ("FLOAT", {"default": 0}),
                "presence_penalty": ("FLOAT", {"default": 0}),
                "timeout": ("INT", {"default": 60}),
            }
        }

    def get_llm_config(
        self,
        base_url,
        api_key,
        llm_model,
        temperature,
        seed,
        max_tokens,
        top_p,
        frequency_penalty,
        presence_penalty,
        timeout,
    ):
        return (
            TaraLLMConfig(
                base_url=base_url,
                api_key=api_key,
                llm_model=llm_model,
                temperature=temperature,
                seed=seed,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                timeout=timeout,
            ),
        )


class TaraPresetLLMConfigNode:
    RETURN_TYPES = ("TARA_LLM_CONFIG",)
    RETURN_NAMES = ("llm_config",)
    FUNCTION = "get_preset_llm_config"
    CATEGORY = "tara-llm"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "llm_models": (get_model_names(MODEL_DICT),),
                "temperature": ("FLOAT", {"default": 0.4}),
                "seed": ("INT", {"default": 42}),
                "max_tokens": ("INT", {"default": 1000}),
                "top_p": ("FLOAT", {"default": 1}),
                "frequency_penalty": ("FLOAT", {"default": 0}),
                "presence_penalty": ("FLOAT", {"default": 0}),
                "timeout": ("INT", {"default": 60}),
                "use_loader": ("BOOLEAN", {"default": True}),
                "loader_temporary": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "api_key": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    @staticmethod
    def get_base_url_for_provider(provider):
        if provider == "groq":
            return "https://api.groq.com/openai/v1"
        elif provider == "openai":
            return "https://api.openai.com/v1"
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_preset_llm_config(
        self,
        llm_models,
        temperature,
        seed,
        max_tokens,
        top_p,
        frequency_penalty,
        presence_penalty,
        timeout,
        use_loader,
        loader_temporary,
        api_key="",
    ):
        provider, llm_model_name = tuple(llm_models.split("/")[:2])

        if use_loader:
            loader = TaraAPIKeyLoader()
            (api_key,) = loader.load_api_key(llm_models, loader_temporary)

        print("DEBUG API KEY::", api_key)

        return (
            TaraLLMConfig(
                base_url=self.get_base_url_for_provider(provider),
                api_key=api_key,
                llm_model=llm_model_name,
                temperature=temperature,
                seed=seed,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                timeout=timeout,
            ),
        )
