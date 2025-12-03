import os
import tensorflow as tf
import sys

# Define model path
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "cnn-parameters-improvement-23-0.91.model")

print(f"Python executable: {sys.executable}")
print(f"TensorFlow version: {tf.__version__}")
print(f"Attempting to load model from: {MODEL_PATH}")

if not os.path.exists(MODEL_PATH):
    print("Model file does not exist at path!")
    sys.exit(1)

try:
    os.environ['TF_USE_LEGACY_KERAS'] = '1'
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    import traceback
    traceback.print_exc()
