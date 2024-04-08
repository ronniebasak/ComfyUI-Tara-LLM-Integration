from .py.tara_master import (
    TaraPrompter,
    TaraAPIKeySaver,
    TaraAPIKeyLoader,
    TaraDaisyChainNode,
)
from .py.tara_advanced import TaraPrompterAdvancedNode, TaraLLMConfigNode
# from .py.

NODE_CLASS_MAPPINGS = {
    "TaraPrompter": TaraPrompter,
    "TaraApiKeyLoader": TaraAPIKeyLoader,
    "TaraApiKeySaver": TaraAPIKeySaver,
    "TaraDaisyChainNode": TaraDaisyChainNode,
    "TaraPrompterAdvanced": TaraPrompterAdvancedNode,
    "TaraLLMConfig": TaraLLMConfigNode,

}
NODE_DISPLAY_NAME_MAPPINGS = {
    "TaraPrompter": "Tara LLM Primary Node",
    "TaraApiKeyLoader": "Tara LLM API Key Loader",
    "TaraApiKeySaver": "Tara LLM API Key Saver",
    "TaraDaisyChainNode": "Tara LLM Daisy Chain Node",
    "TaraPrompterAdvanced": "Tara LLM Advanced Node",
    "TaraLLMConfig": "Tara LLM Config Node",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
