from .py.tara_master import (
    TaraPrompter,
    TaraAPIKeySaver,
    TaraAPIKeyLoader,
    TaraDaisyChainNode,
)
from .py.tara_advanced import TaraPrompterAdvancedNode, TaraLLMConfigNode, TaraAdvancedCompositionNode, TaraPresetLLMConfigNode
# from .py.

NODE_CLASS_MAPPINGS = {
    "TaraPrompter": TaraPrompter,
    "TaraApiKeyLoader": TaraAPIKeyLoader,
    "TaraApiKeySaver": TaraAPIKeySaver,
    "TaraDaisyChainNode": TaraDaisyChainNode,
    "TaraPrompterAdvanced": TaraPrompterAdvancedNode,
    "TaraLLMConfig": TaraLLMConfigNode,
    "TaraPresetLLMConfig": TaraPresetLLMConfigNode,
    "TaraAdvancedComposition": TaraAdvancedCompositionNode,
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "TaraPrompterAdvanced": "Tara Advanced LLM Node",
    "TaraAdvancedComposition": "Tara Advanced LLM Composition Node",
    "TaraApiKeyLoader": "Tara LLM API Key Loader",
    "TaraApiKeySaver": "Tara LLM API Key Saver",
    "TaraLLMConfig": "Tara LLM Config Node",
    "TaraPresetLLMConfig": "Tara Preset LLM Config Node",

    "TaraPrompter": "(Deprecated) Tara LLM Primary Node",
    "TaraDaisyChainNode": "(Deprecated) Tara LLM Daisy Chain Node (Deprecated)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
