import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Psikolojik Test API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Model yapılandırması
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/mental_health_xgboost_v1.pkl")
    
    # Gemini API yapılandırması
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")
    
    # CORS yapılandırması
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Loglama seviyesi
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()