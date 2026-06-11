import os
import json
import pandas as pd
import numpy as np
import tempfile
import tensorflow as tf
import zipfile
from PIL import Image


class MLModelAdapter:
    def __init__(
        self,
        model_path: str = "best_model_skenario3.keras",
        mapping_path: str = "class_mapping.csv"
    ):
        self.model_path = model_path
        self.mapping_path = mapping_path

        self.classes = self._load_class_mapping()
        self.model = self._load_model()

    def _load_class_mapping(self):
        try:
            df = pd.read_csv(self.mapping_path)

            if "index" in df.columns:
                df = df.sort_values("index")

            return df["class_name"].tolist()

        except Exception as e:
            print(f"Error loading class mapping: {e}")
            return [
                "Broken soybeans",
                "Immature soybeans",
                "Intact soybeans",
                "Skin-damaged soybeans",
                "Spotted soybeans"
            ]

    def _load_model(self):
        try:
            return tf.keras.models.load_model(
                self.model_path,
                compile=False,
                safe_mode=False
            )
        except Exception as e:
            if "quantization_config" not in str(e):
                print(f"Error loading model {self.model_path}: {e}")
                raise e

            print("Model config contains unsupported quantization_config. Loading a compatible temporary copy.")
            compatible_model_path = self._create_compatible_model_copy()
            try:
                return tf.keras.models.load_model(
                    compatible_model_path,
                    compile=False,
                    safe_mode=False
                )
            except Exception as fallback_error:
                print(f"Error loading compatible model copy {compatible_model_path}: {fallback_error}")
                raise fallback_error
            finally:
                try:
                    os.remove(compatible_model_path)
                except OSError:
                    pass

    def _create_compatible_model_copy(self) -> str:
        def remove_unsupported_config(value):
            if isinstance(value, dict):
                value.pop("quantization_config", None)
                for child in value.values():
                    remove_unsupported_config(child)
            elif isinstance(value, list):
                for child in value:
                    remove_unsupported_config(child)

        with tempfile.NamedTemporaryFile(suffix=".keras", delete=False) as temp_file:
            compatible_model_path = temp_file.name

        with zipfile.ZipFile(self.model_path, "r") as source:
            with zipfile.ZipFile(compatible_model_path, "w") as target:
                for item in source.infolist():
                    content = source.read(item.filename)
                    if item.filename == "config.json":
                        config = json.loads(content.decode("utf-8"))
                        remove_unsupported_config(config)
                        content = json.dumps(config).encode("utf-8")
                    target.writestr(item, content)

        return compatible_model_path

    def predict(self, img: Image.Image) -> tuple[str, float]:
        if img.mode != "RGB":
            img = img.convert("RGB")

        img = img.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)

        # Untuk EfficientNet TensorFlow/Keras, pakai preprocess_input
        img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)

        img_tensor = np.expand_dims(img_array, axis=0)

        predictions = self.model.predict(img_tensor, verbose=0)

        idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][idx]) * 100

        class_name = self.classes[idx] if idx < len(self.classes) else "Unknown"

        return class_name, confidence
