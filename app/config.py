from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/personal_life_os"
    GROQ_API_KEY: str = ""
    SYSTEM_NAME: str = "Orin"

    class Config:
        env_file = ".env"

settings = Settings()
