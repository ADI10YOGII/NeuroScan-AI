# simple_test.py
import os
# Set compatibility flags
os.environ['TF_USE_LEGACY_KERAS'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import cv2
import numpy as np

def simple_predict(image_path):
    """Simple prediction function that should work"""
    try:
        # Load the original model directly
        model = tf.keras.models.load_model(
            'models/cnn-parameters-improvement-23-0.91.model',
            compile=False
        )
        
        print("✅ Original model loaded successfully!")
        
        # Process image
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Could not load image: {image_path}")
            return None, None
            
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (240, 240))
        image = image / 255.0
        image = np.expand_dims(image, axis=0)
        
        # Predict
        prediction = model.predict(image, verbose=0)[0][0]
        
        # Results
        if prediction > 0.5:
            result = "Tumor Detected (YES)"
            confidence = prediction
        else:
            result = "No Tumor Detected (NO)"
            confidence = 1 - prediction
        
        print(f"🧠 {result}")
        print(f"📊 Confidence: {confidence:.2%}")
        return result, confidence
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

# Test the simple approach
if __name__ == "__main__":
    print("🧠 Simple Brain Tumor Detection Test")
    print("=" * 40)
    result, confidence = simple_predict(r'test_images\no.jpeg')
    
    if result:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")