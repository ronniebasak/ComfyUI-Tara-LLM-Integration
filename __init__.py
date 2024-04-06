from .py.tara_master import (
    TaraPrompter,
    TaraAPIKeySaver,
    TaraAPIKeyLoader,
    TaraDaisyChainNode,
)

NODE_CLASS_MAPPINGS = {
    "TaraMaster": TaraPrompter,
    "TaraApiKeyLoader": TaraAPIKeyLoader,
    "TaraApiKeySaver": TaraAPIKeySaver,
    "TaraDaisyChainNode": TaraDaisyChainNode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "TaraMaster": "Tara LLM Primary Node",
    "TaraApiKeyLoader": "Tara LLM API Key Loader",
    "TaraApiKeySaver": "Tara LLM API Key Saver",
    "TaraDaisyChainNode": "Tara LLM Daisy Chain Node",
}
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
