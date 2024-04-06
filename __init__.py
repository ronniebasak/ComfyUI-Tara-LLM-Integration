from .groq_master import (
    GroqMaster,
    GroqAPIKeySaver,
    GroqAPIKeyLoader,
    GroqDaisyChainNode,
)

NODE_CLASS_MAPPINGS = {
    "groqMaster": GroqMaster,
    "groqApiKeyLoader": GroqAPIKeyLoader,
    "groqApiKeySaver": GroqAPIKeySaver,
    "groqDaisyChainNode": GroqDaisyChainNode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "groqMaster": "Groq Master",
    "groqApiKeyLoader": "Groq API Key Loader",
    "groqApiKeySaver": "Groq API Key Saver",
    "groqDaisyChainNode": "Groq Daisy Chain Node",
}
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
