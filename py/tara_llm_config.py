class TaraLLMConfig:
    base_url: str = "https://api.openai.com/v1"
    api_key: str = "sk-<your-api-key>"
    llm_model: str = "gpt-3.5-turbo"
    temperature: float = 0.4
    seed: int = 42
    max_tokens: int = 1024
    top_p: int = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    timeout: int = 60

    def __init__(
        self,
        base_url: str,
        api_key: str,
        llm_model: str,
        seed: int,
        temperature: float,
        max_tokens: int,
        top_p: int,
        frequency_penalty: float,
        presence_penalty: float,
        timeout: int,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.llm_model = llm_model
        self.temperature = temperature
        self.seed = seed
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.timeout = timeout
