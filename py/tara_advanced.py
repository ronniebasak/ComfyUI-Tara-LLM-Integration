import openai
import orjson
import os.path
import os
from .tara_llm_config import TaraLLMConfig
from .tara_master import get_llm_config, META_PROMPT, post_process_prompt


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

    def configure_chat_creation(self, llm_config, messages, overrides):
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
