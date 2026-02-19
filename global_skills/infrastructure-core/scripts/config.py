"""
Configuration Module - The Dude S.A.S.
Centralized configuration with Pydantic v2 validation.
Uses environment variables for all sensitive data.
"""
import os
from pathlib import Path
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig:
    """Environment configuration base"""
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )


class SupabaseConfig(EnvConfig):
    """Supabase configuration"""
    url: str = Field(default="https://fmcgnrjkyecppxquijvj.supabase.co", alias="SUPABASE_URL")
    anon_key: str = Field(..., alias="SUPABASE_ANON_KEY")
    
    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith("https://"):
            raise ValueError("Supabase URL must start with https://")
        return v


class RedisConfig(EnvConfig):
    """Redis configuration"""
    host: str = Field(default="localhost", alias="REDIS_HOST")
    port: int = Field(default=6379, alias="REDIS_PORT")
    db: int = Field(default=0, alias="REDIS_DB")
    password: Optional[str] = Field(default=None, alias="REDIS_PASSWORD")


class TelegramConfig(EnvConfig):
    """Telegram configuration"""
    api_id: Optional[int] = Field(default=None, alias="TELEGRAM_API_ID")
    api_hash: Optional[str] = Field(default=None, alias="TELEGRAM_API_HASH")
    
    @field_validator("api_id")
    @classmethod
    def validate_api_id(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v <= 0:
            raise ValueError("Telegram API ID must be positive")
        return v


class OpenAIConfig(EnvConfig):
    """OpenAI configuration"""
    api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")


class GroqConfig(EnvConfig):
    """Groq configuration"""
    api_key: Optional[str] = Field(default=None, alias="GROQ_API_KEY")


class OllamaConfig(EnvConfig):
    """Ollama configuration"""
    base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    model: str = Field(default="llama3.1:8b", alias="OLLAMA_MODEL")


class TwilioConfig(EnvConfig):
    """Twilio configuration"""
    account_sid: Optional[str] = Field(default=None, alias="TWILIO_ACCOUNT_SID")
    auth_token: Optional[str] = Field(default=None, alias="TWILIO_AUTH_TOKEN")
    whatsapp_number: Optional[str] = Field(default=None, alias="TWILIO_WHATSAPP_NUMBER")


class PineconeConfig(EnvConfig):
    """Pinecone configuration"""
    api_key: Optional[str] = Field(default=None, alias="PINECONE_API_KEY")
    environment: Optional[str] = Field(default=None, alias="PINECONE_ENVIRONMENT")


class FirecrawlConfig(EnvConfig):
    """Firecrawl configuration"""
    api_key: Optional[str] = Field(default=None, alias="FIRECRAWL_API_KEY")


class ExaConfig(EnvConfig):
    """Exa configuration"""
    api_key: Optional[str] = Field(default=None, alias="EXA_API_KEY")


class Context7Config(EnvConfig):
    """Context7 configuration"""
    api_key: Optional[str] = Field(default=None, alias="CTX7_API_KEY")


class E2BConfig(EnvConfig):
    """E2B configuration"""
    api_key: Optional[str] = Field(default=None, alias="E2B_API_KEY")


class StripeConfig(EnvConfig):
    """Stripe configuration"""
    api_key: Optional[str] = Field(default=None, alias="STRIPE_API_KEY")
    webhook_secret: Optional[str] = Field(default=None, alias="STRIPE_WEBHOOK_SECRET")
    payment_link: Optional[str] = Field(default=None, alias="STRIPE_PAYMENT_LINK")


class EmailConfig(EnvConfig):
    """Email configuration"""
    smtp_host: Optional[str] = Field(default=None, alias="SMTP_HOST")
    smtp_port: Optional[int] = Field(default=None, alias="SMTP_PORT")
    smtp_user: Optional[str] = Field(default=None, alias="SMTP_USER")
    smtp_password: Optional[str] = Field(default=None, alias="SMTP_PASSWORD")


class PathConfig(EnvConfig):
    """Path configuration"""
    root_dir: Path = Field(default=Path(__file__).parent.parent, alias="ROOT_DIR")
    data_dir: Path = Field(default=Path(__file__).parent.parent / "data", alias="DATA_DIR")
    db_dir: Path = Field(default=Path(__file__).parent.parent / "dude-db", alias="DB_DIR")
    workspace_dir: Path = Field(default=Path(__file__).parent.parent / "workspace", alias="WORKSPACE_DIR")
    logs_dir: Path = Field(default=Path(__file__).parent.parent / "logs", alias="LOGS_DIR")
    
    @field_validator("*", mode="before")
    @classmethod
    def validate_paths(cls, v):
        if isinstance(v, str):
            v = Path(v)
        return v


class Config(BaseSettings):
    """Main configuration class"""
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )
    
    supabase: SupabaseConfig = Field(default_factory=SupabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    groq: GroqConfig = Field(default_factory=GroqConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    twilio: TwilioConfig = Field(default_factory=TwilioConfig)
    pinecone: PineconeConfig = Field(default_factory=PineconeConfig)
    firecrawl: FirecrawlConfig = Field(default_factory=FirecrawlConfig)
    exa: ExaConfig = Field(default_factory=ExaConfig)
    context7: Context7Config = Field(default_factory=Context7Config)
    e2b: E2BConfig = Field(default_factory=E2BConfig)
    stripe: StripeConfig = Field(default_factory=StripeConfig)
    email: EmailConfig = Field(default_factory=EmailConfig)
    paths: PathConfig = Field(default_factory=PathConfig)
    
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")
    
    class Config:
        arbitrary_types_allowed = True


_global_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration singleton"""
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def reload_config() -> Config:
    """Reload configuration from environment"""
    global _global_config
    _global_config = Config()
    return _global_config
