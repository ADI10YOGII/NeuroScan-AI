import tensorflow as tf
import os

# Define model path
MODEL_PATH = os.path.join("models", "cnn-parameters-improvement-23-0.91.model")

try:
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    model.summary()
    
    print("\nLayer Names:")
    for layer in model.layers:
        print(f"- {layer.name} ({layer.__class__.__name__})")
        
except Exception as e:
    print(f"Error: {e}")
