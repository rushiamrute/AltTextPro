from enum import Enum
from dataclasses import dataclass

class ModelType(Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    HUGGINGFACE = "huggingface"

@dataclass
class ModelConfig:
    OPENAI_MODEL = "gpt-4-1106-vision-preview"
    GEMINI_MODEL = "gemini-1.5-pro-vision"
    HUGGINGFACE_MODEL = "Salesforce/blip-image-captioning-large"
    DEFAULT_MODEL = ModelType.HUGGINGFACE 