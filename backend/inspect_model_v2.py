import tensorflow as tf
import os
import sys

# Set env vars like in backend
os.environ['TF_USE_LEGACY_KERAS'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Define absolute model path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "backend", "models", "cnn-parameters-improvement-23-0.91.model")

print(f"Loading model from: {MODEL_PATH}")

try:
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    model.summary()
    
    print("\nLayer Names:")
    for layer in model.layers:
        print(f"- {layer.name} ({layer.__class__.__name__})")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
