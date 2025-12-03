# batch_correct_test.py
import os
os.environ['TF_USE_LEGACY_KERAS'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

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

def load_model_once():
    """Load the model once and reuse it for all predictions"""
    try:
        model = tf.keras.models.load_model(
            'models/cnn-parameters-improvement-23-0.91.model',
            compile=False
        )
        print("✅ Model loaded successfully!")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

def process_single_image(model, image_path, show_steps=False):
    """Process a single image and return prediction results"""
    try:
        # Load original image
        original_image = cv2.imread(image_path)
        if original_image is None:
            print(f"❌ Could not load image: {image_path}")
            return None
        
        if show_steps:
            # Show preprocessing steps for individual image
            plt.figure(figsize=(15, 10))
            
            # Original image
            plt.subplot(2, 3, 1)
            plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
            plt.title(f"1. Original: {os.path.basename(image_path)}")
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
        
        # Step 3: Convert to RGB
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
        
        # Predict
        prediction = model.predict(final_image, verbose=0)[0][0]
        
        # Results
        if prediction > 0.5:
            result = "Tumor Detected (YES)"
            confidence = prediction
            emoji = "🟢"
            color = 'red'
        else:
            result = "No Tumor Detected (NO)"
            confidence = 1 - prediction
            emoji = "🔴"
            color = 'green'
        
        if show_steps:
            plt.subplot(2, 3, 6)
            plt.imshow(normalized_image)
            plt.title(f"6. Prediction: {result}\nConfidence: {confidence:.2%}", 
                     fontweight='bold', color=color)
            plt.axis('off')
            
            plt.tight_layout()
            plt.show()
        
        return {
            'filename': os.path.basename(image_path),
            'result': result,
            'confidence': confidence,
            'emoji': emoji,
            'raw_score': prediction
        }
        
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None

def process_test_images_folder(show_individual_steps=False, show_summary_plot=True):
    """Process all images in the test_images folder"""
    test_folder = "test_images"
    
    # Check if test folder exists
    if not os.path.exists(test_folder):
        print(f"❌ Test folder '{test_folder}' not found!")
        print(f"📁 Current directory: {os.getcwd()}")
        print(f"📁 Available folders: {[f for f in os.listdir('.') if os.path.isdir(f)]}")
        return
    
    # Get all image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')
    image_files = []
    
    for file in os.listdir(test_folder):
        if file.lower().endswith(image_extensions):
            image_files.append(os.path.join(test_folder, file))
    
    if not image_files:
        print(f"❌ No image files found in '{test_folder}' folder!")
        print(f"📁 Contents of '{test_folder}': {os.listdir(test_folder)}")
        return
    
    print(f"📁 Found {len(image_files)} images in '{test_folder}' folder")
    
    # Load model once
    model = load_model_once()
    if model is None:
        return
    
    print("\n🧠 Starting Batch Processing with Brain Cropping")
    print("=" * 60)
    
    # Process each image
    results = []
    for i, image_path in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] Processing: {os.path.basename(image_path)}")
        
        result = process_single_image(model, image_path, show_steps=show_individual_steps)
        
        if result:
            results.append(result)
            print(f"   {result['emoji']} {result['result']}")
            print(f"   📊 Confidence: {result['confidence']:.2%}")
        else:
            print(f"   ❌ Failed to process")
    
    # Print summary
    print_summary(results)
    
    # Show summary plot if requested
    if show_summary_plot and results:
        show_batch_results(results)

def print_summary(results):
    """Print a formatted summary of all results"""
    if not results:
        print("\n❌ No images were successfully processed")
        return
    
    print("\n" + "=" * 60)
    print("📊 BATCH PREDICTION SUMMARY")
    print("=" * 60)
    
    tumor_count = sum(1 for r in results if "Tumor" in r['result'])
    no_tumor_count = len(results) - tumor_count
    
    # Sort results by confidence (highest first)
    results_sorted = sorted(results, key=lambda x: x['confidence'], reverse=True)
    
    for res in results_sorted:
        status = "YES" if "Tumor" in res['result'] else "NO"
        print(f"{res['emoji']} {res['filename']:25} {status:5} {res['confidence']:.2%}")
    
    print("-" * 60)
    print(f"📈 Total Images Processed: {len(results)}")
    print(f"🟢 With Tumor: {tumor_count}")
    print(f"🔴 Without Tumor: {no_tumor_count}")
    
    if len(results) > 0:
        tumor_rate = tumor_count / len(results) * 100
        print(f"📊 Tumor Detection Rate: {tumor_rate:.1f}%")
        
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        print(f"📊 Average Confidence: {avg_confidence:.2%}")

def show_batch_results(results):
    """Display a grid of sample results with predictions"""
    try:
        # Take first 4 results to display
        display_results = results[:4]
        
        plt.figure(figsize=(15, 12))
        
        for i, result in enumerate(display_results):
            image_path = os.path.join("test_images", result['filename'])
            image = cv2.imread(image_path)
            
            if image is not None:
                # Process image for display (crop and resize)
                cropped = smart_crop_brain(image)
                resized = cv2.resize(cropped, (200, 200))
                rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                normalized = rgb / 255.0
                
                plt.subplot(2, 2, i + 1)
                plt.imshow(normalized)
                plt.title(f"{result['emoji']} {result['filename']}\n{result['result']}\nConfidence: {result['confidence']:.2%}", 
                         fontsize=10, fontweight='bold',
                         color='red' if "Tumor" in result['result'] else 'green')
                plt.axis('off')
        
        plt.suptitle("Brain Tumor Detection - Sample Results", fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"ℹ️  Could not display summary plot: {e}")

def main():
    """Main function with user options"""
    print("🧠 Brain Tumor Detection - Batch Processing")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Process all images (quick mode)")
        print("2. Process all images with detailed steps for each image")
        print("3. Process all images with summary plot")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            process_test_images_folder(show_individual_steps=False, show_summary_plot=False)
        elif choice == '2':
            process_test_images_folder(show_individual_steps=True, show_summary_plot=False)
        elif choice == '3':
            process_test_images_folder(show_individual_steps=False, show_summary_plot=True)
        elif choice == '4':
            print("👋 Thank you for using Brain Tumor Detection!")
            break
        else:
            print("❌ Invalid choice! Please enter 1-4.")

if __name__ == "__main__":
    # Run directly with quick processing
    process_test_images_folder(show_individual_steps=False, show_summary_plot=True)
    
    # Uncomment the line below for interactive mode
    # main()