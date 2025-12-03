# correct_test.py
import os
os.environ['TF_USE_LEGACY_KERAS'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt

def crop_brain_region(image):
    """
    Crop the image to focus on the brain region
    This is a simplified version - you might need to adjust based on your images
    """
    # Convert to grayscale for processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to isolate brain region
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        # If no contours found, return center crop
        print("⚠️ No brain region detected, using center crop")
        h, w = image.shape[:2]
        crop_size = min(h, w) * 0.8  # 80% of smaller dimension
        start_x = int((w - crop_size) // 2)
        start_y = int((h - crop_size) // 2)
        cropped = image[start_y:start_y+int(crop_size), start_x:start_x+int(crop_size)]
    else:
        # Get the largest contour (assumed to be the brain)
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Add some padding
        padding = 10
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + 2 * padding)
        h = min(image.shape[0] - y, h + 2 * padding)
        
        cropped = image[y:y+h, x:x+w]
    
    return cropped

def smart_crop_brain(image):
    """
    Alternative brain cropping method using edge detection
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Canny edge detection
    edges = cv2.Canny(blurred, 30, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour that's likely the brain
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # Try to find a reasonably sized contour (not too small, not the whole image)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area_ratio = cv2.contourArea(contour) / (image.shape[0] * image.shape[1])
            
            # Look for contours that are between 10% and 80% of image area (likely brain)
            if 0.1 < area_ratio < 0.8:
                # Add padding
                padding = 15
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = min(image.shape[1] - x, w + 2 * padding)
                h = min(image.shape[0] - y, h + 2 * padding)
                
                cropped = image[y:y+h, x:x+w]
                return cropped
    
    # Fallback: center crop
    print("⚠️ Using center crop fallback")
    h, w = image.shape[:2]
    crop_size = min(h, w) * 0.7
    start_x = int((w - crop_size) // 2)
    start_y = int((h - crop_size) // 2)
    return image[start_y:start_y+int(crop_size), start_x:start_x+int(crop_size)]

def correct_predict(image_path, show_steps=False):
    """Correct prediction with proper brain cropping"""
    try:
        # Load model
        model = tf.keras.models.load_model(
            'models/cnn-parameters-improvement-23-0.91.model',
            compile=False
        )
        
        print("✅ Model loaded successfully!")
        
        # Load original image
        original_image = cv2.imread(image_path)
        if original_image is None:
            print(f"❌ Could not load image: {image_path}")
            return None, None
        
        if show_steps:
            # Show preprocessing steps
            plt.figure(figsize=(15, 10))
            
            # Original image
            plt.subplot(2, 3, 1)
            plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
            plt.title("1. Original Image")
            plt.axis('off')
        
        # Step 1: Crop brain region
        cropped_brain = smart_crop_brain(original_image)
        
        if show_steps:
            plt.subplot(2, 3, 2)
            plt.imshow(cv2.cvtColor(cropped_brain, cv2.COLOR_BGR2RGB))
            plt.title("2. Cropped Brain Region")
            plt.axis('off')
        
        # Step 2: Resize to 240x240
        resized_image = cv2.resize(cropped_brain, (240, 240))
        
        if show_steps:
            plt.subplot(2, 3, 3)
            plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
            plt.title("3. Resized to 240x240")
            plt.axis('off')
        
        # Step 3: Convert to RGB (if needed)
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        
        # Step 4: Normalize to [0, 1]
        normalized_image = rgb_image / 255.0
        
        if show_steps:
            plt.subplot(2, 3, 4)
            plt.imshow(normalized_image)
            plt.title("4. Normalized [0,1]")
            plt.axis('off')
            
            # Show pixel value distribution
            plt.subplot(2, 3, 5)
            plt.hist(normalized_image.ravel(), bins=50, alpha=0.7)
            plt.title("5. Pixel Value Distribution")
            plt.xlabel("Pixel Value")
            plt.ylabel("Frequency")
        
        # Step 5: Add batch dimension
        final_image = np.expand_dims(normalized_image, axis=0)
        
        print(f"📦 Final input shape: {final_image.shape}")
        
        # Predict
        prediction = model.predict(final_image, verbose=0)[0][0]
        
        # Results
        if prediction > 0.5:
            result = "Tumor Detected (YES)"
            confidence = prediction
            color = 'red'
        else:
            result = "No Tumor Detected (NO)"
            confidence = 1 - prediction
            color = 'green'
        
        if show_steps:
            plt.subplot(2, 3, 6)
            plt.imshow(normalized_image)
            plt.title(f"6. Prediction: {result}\nConfidence: {confidence:.2%}", 
                     fontweight='bold', color=color)
            plt.axis('off')
            
            plt.tight_layout()
            plt.show()
        
        print(f"\n🧠 Result: {result}")
        print(f"📊 Confidence: {confidence:.2%}")
        print(f"🔢 Raw score: {prediction:.6f}")
        
        return result, confidence
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def compare_methods(image_path):
    """Compare results with and without brain cropping"""
    print("🔄 Testing with brain cropping...")
    result_cropped, confidence_cropped = correct_predict(image_path, show_steps=True)
    
    print("\n" + "="*50)
    print("🔄 Testing without brain cropping (original method)...")
    
    # Original method without cropping
    model = tf.keras.models.load_model(
        'models/cnn-parameters-improvement-23-0.91.model',
        compile=False
    )
    
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (240, 240))  # No cropping!
    image = image / 255.0
    image_batch = np.expand_dims(image, axis=0)
    
    prediction = model.predict(image_batch, verbose=0)[0][0]
    
    if prediction > 0.5:
        result_original = "Tumor Detected (YES)"
        confidence_original = prediction
    else:
        result_original = "No Tumor Detected (NO)"
        confidence_original = 1 - prediction
    
    print(f"🧠 Result (no crop): {result_original}")
    print(f"📊 Confidence (no crop): {confidence_original:.2%}")
    
    print("\n" + "="*50)
    print("📊 COMPARISON RESULTS:")
    print(f"With brain cropping:    {result_cropped} ({confidence_cropped:.2%})")
    print(f"Without brain cropping: {result_original} ({confidence_original:.2%})")

if __name__ == "__main__":
    print("🧠 Correct Brain Tumor Detection with Brain Cropping")
    print("=" * 60)
    
    # Test with visualization
    result, confidence = correct_predict(r'test_images\no.jpeg', show_steps=True)
    
    # Uncomment to compare methods
    # compare_methods(r'test_images\no.jpeg')
    
    if result:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")