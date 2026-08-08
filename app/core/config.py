import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    DATABASE_URL = os.getenv("DATABASE_URL", "abtalks.db")
    DISCOVERY_INTERVAL_MINUTES = int(os.getenv("DISCOVERY_INTERVAL_MINUTES", "2"))
    
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")
    LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/llama-3.1-8b-instruct")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

settings = Settings()
