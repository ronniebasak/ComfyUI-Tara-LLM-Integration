from .tara_master import (
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
    "TaraMaster": "Tara Master",
    "TaraApiKeyLoader": "Tara API Key Loader",
    "TaraApiKeySaver": "Tara API Key Saver",
    "TaraDaisyChainNode": "Tara Daisy Chain Node",
}
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
