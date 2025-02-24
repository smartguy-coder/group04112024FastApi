from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    USER_MONGO: str
    PASSWORD_MONGO: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def MONGO_URI(self) -> str:
        return f"mongodb+srv://{self.USER_MONGO}:{self.PASSWORD_MONGO}@myclustrer.dqcod.mongodb.net/?retryWrites=true&w=majority&appName=myClustrer"


settings = Settings()
