# debug_test.py
import os
os.environ['TF_USE_LEGACY_KERAS'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt

def debug_predict(image_path):
    """Debug prediction with detailed information"""
    try:
        # Load model
        model = tf.keras.models.load_model(
            'models/cnn-parameters-improvement-23-0.91.model',
            compile=False
        )
        
        print("✅ Model loaded successfully!")
        
        # Load and analyze image
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Could not load image: {image_path}")
            return
        
        print(f"📐 Original image shape: {image.shape}")
        print(f"🎨 Image type: {image.dtype}")
        print(f"📊 Pixel range: [{image.min()}, {image.max()}]")
        
        # Display original image
        plt.figure(figsize=(15, 5))
        
        plt.subplot(1, 3, 1)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title(f"Original Image\n{os.path.basename(image_path)}")
        plt.axis('off')
        
        # Preprocess image
        image_processed = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_processed = cv2.resize(image_processed, (240, 240))
        
        plt.subplot(1, 3, 2)
        plt.imshow(image_processed)
        plt.title("After Resize (240x240)")
        plt.axis('off')
        
        image_processed = image_processed / 255.0
        print(f"📊 Pixel range after normalization: [{image_processed.min():.3f}, {image_processed.max():.3f}]")
        
        # Prepare for prediction
        image_batch = np.expand_dims(image_processed, axis=0)
        print(f"📦 Batch shape for prediction: {image_batch.shape}")
        
        # Make prediction
        prediction = model.predict(image_batch, verbose=0)
        print(f"🔍 Raw prediction output: {prediction}")
        print(f"📏 Prediction shape: {prediction.shape}")
        
        prediction_value = prediction[0][0]
        print(f"🎯 Final prediction value: {prediction_value:.6f}")
        
        # Interpret results
        if prediction_value > 0.5:
            result = "Tumor Detected (YES)"
            confidence = prediction_value
        else:
            result = "No Tumor Detected (NO)"
            confidence = 1 - prediction_value
        
        plt.subplot(1, 3, 3)
        plt.imshow(image_processed)
        plt.title(f"Prediction: {result}\nConfidence: {confidence:.2%}", 
                 fontweight='bold', color='red' if prediction_value > 0.5 else 'green')
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        print(f"\n🧠 Result: {result}")
        print(f"📊 Confidence: {confidence:.2%}")
        print(f"🔢 Raw score: {prediction_value:.6f}")
        
        return result, confidence
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def test_multiple_images():
    """Test multiple images to see if the issue is consistent"""
    test_images = [
        r'test_images\no.jpeg',      # Should be NO tumor
        r'no\1 no.jpeg',             # Original NO tumor from dataset
        r'yes\Y3.jpg',               # Original YES tumor from dataset
    ]
    
    for image_path in test_images:
        if os.path.exists(image_path):
            print(f"\n{'='*60}")
            print(f"Testing: {image_path}")
            print(f"{'='*60}")
            debug_predict(image_path)
        else:
            print(f"⚠️ Image not found: {image_path}")

if __name__ == "__main__":
    print("🔍 Debugging Brain Tumor Detection")
    print("=" * 50)
    
    # Test the problematic image
    debug_predict(r'test_images\no.jpeg')
    
    # Uncomment to test multiple images
    # test_multiple_images()