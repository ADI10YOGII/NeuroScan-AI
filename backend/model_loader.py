import tensorflow as tf
import os

class ModelLoader:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance

    def load_model(self, model_path: str):
        if self._model is None:
            try:
                # Set environment variables to avoid some TF warnings/errors
                os.environ['TF_USE_LEGACY_KERAS'] = '1'
                os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
                
                self._model = tf.keras.models.load_model(model_path, compile=False)
                print(f"✅ Model loaded successfully from {model_path}")
            except Exception as e:
                print(f"❌ Error loading model: {e}")
                raise e
        return self._model

    def get_model(self):
        return self._model

model_loader = ModelLoader()
