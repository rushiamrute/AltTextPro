from PIL import Image
import io
from app.core.model_config import ModelType
from app.services.vision_factory import VisionModelFactory
from app.core.exceptions import VisionError

class VisionService:
    def __init__(self, model_type: ModelType = ModelType.GEMINI):
        print(f"Initializing VisionService with model type: {model_type}")  # Debug log
        self.model = VisionModelFactory.get_model(model_type)

    def generate_alt_text(self, image_bytes: bytes) -> str:
        try:
            print("Processing image in VisionService")  # Debug log
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            return self.model.generate_alt_text(image)
        except Exception as e:
            print(f"Error in VisionService: {str(e)}")  # Debug log
            raise VisionError(f"Error generating alt text: {str(e)}")

    def switch_model(self, model_type: ModelType):
        print(f"Switching to model type: {model_type}")  # Debug log
        self.model = VisionModelFactory.get_model(model_type)