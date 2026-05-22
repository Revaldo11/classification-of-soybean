import os
import pandas as pd
import numpy as np
import tensorflow as tf
from PIL import Image

class MLModelAdapter:
    def __init__(self, model_path: str = "best_model_skenario3.keras", mapping_path: str = "class_mapping.csv"):
        self.model_path = model_path
        self.mapping_path = mapping_path
        
        # Load class mapping
        self.classes = self._load_class_mapping()
        
        # Load model
        self.model = self._load_model()

    def _load_class_mapping(self):
        """Loads class names from a CSV file."""
        try:
            df = pd.read_csv(self.mapping_path)
            # Ensure it's sorted by index if available
            if 'index' in df.columns:
                df = df.sort_values('index')
            return df['class_name'].tolist()
        except Exception as e:
            print(f"Error loading class mapping: {e}")
            # Fallback classes if CSV fails (matching previous implementation)
            return [
                "Broken soybeans",
                "Immature soybeans",
                "Intact soybeans",
                "Skin-damaged soybeans",
                "Spotted soybeans"
            ]

    def _load_model(self):
        """Load the TensorFlow/Keras model."""
        try:
            model = tf.keras.models.load_model(self.model_path)
            return model
        except Exception as e:
            print(f"Error loading model {self.model_path}: {e}")
            raise e

    def predict(self, img: Image.Image) -> tuple[str, float]:
        """Preprocesses the image and performs prediction."""
        if img.mode == 'RGBA':
            img = img.convert('RGB')
            
        # Preprocessing: Resize to 224x224
        img = img.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        
        # BGR Conversion: Many models trained with OpenCV expect BGR instead of RGB.
        # Flipping the last axis (channels).
        img_array = img_array[..., ::-1]
        
        # The model has internal Rescaling and Normalization layers.
        # Passing raw [0, 255] BGR values.
        
        img_tensor = np.expand_dims(img_array, axis=0)
        
        # Predict
        predictions = self.model.predict(img_tensor, verbose=0)
        idx = np.argmax(predictions[0])
        confidence = float(predictions[0][idx]) * 100
        
        class_name = self.classes[idx] if idx < len(self.classes) else "Unknown"
        return class_name, confidence
