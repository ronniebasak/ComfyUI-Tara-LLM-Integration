from .groq_master import GroqMaster, GroqAPIKeySaver, GroqAPIKeyLoader
NODE_CLASS_MAPPINGS = { "groqMaster" : GroqMaster, "groqApiKeyLoader": GroqAPIKeyLoader, "groqApiKeySaver": GroqAPIKeySaver}
NODE_DISPLAY_NAME_MAPPINGS = { "groqMaster" : "Groq Master", "groqApiKeyLoader": "Groq API Key Loader", "groqApiKeySaver": "Groq API Key Saver"}
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']