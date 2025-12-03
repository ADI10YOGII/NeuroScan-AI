# simple_batch_test.py
import os
os.environ['TF_USE_LEGACY_KERAS'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import cv2
import numpy as np

def test_all_images():
    """Test all images in test_Images folder"""
    test_folder = "test_Images"
    
    if not os.path.exists(test_folder):
        print(f"❌ Folder '{test_folder}' not found!")
        return
    
    # Load model
    model = tf.keras.models.load_model(
        'models/cnn-parameters-improvement-23-0.91.model',
        compile=False
    )
    
    # Get all images
    images = []
    for file in os.listdir(test_folder):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            images.append(file)
    
    if not images:
        print(f"❌ No images found in '{test_folder}'")
        return
    
    print(f"🧠 Testing {len(images)} images from '{test_folder}'")
    print("=" * 50)
    
    for image_file in images:
        image_path = os.path.join(test_folder, image_file)
        
        # Process and predict
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (240, 240))
        image = image / 255.0
        image = np.expand_dims(image, axis=0)
        
        prediction = model.predict(image, verbose=0)[0][0]
        
        if prediction > 0.5:
            result = "YES"
            confidence = prediction
            emoji = "🟢"
        else:
            result = "NO"
            confidence = 1 - prediction
            emoji = "🔴"
        
        print(f"{emoji} {image_file:25} → {result:3} ({confidence:.2%})")

if __name__ == "__main__":
    test_all_images()