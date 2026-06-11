from PIL import Image
from src.adapters.ml_model import MLModelAdapter
from src.domain.entities import get_metadata


class PredictSoybeanUseCase:
    def __init__(self, ml_adapter: MLModelAdapter):
        self.ml_adapter = ml_adapter

    def execute(self, image: Image.Image) -> dict:
        label, confidence = self.ml_adapter.predict(image)

        final_label = label
        final_conf = round(confidence, 2)

        if confidence < 75.0:
            final_label = "Bukan Biji Kedelai"
            final_conf = "-"

        metadata = get_metadata(final_label)

        return {
            "label": final_label,
            "confidence": final_conf,
            "grade": metadata["grade"],
            "definition": metadata["definition"],
            "nutrition": metadata["nutrition"],
            "benefits": metadata["benefits"]
        }