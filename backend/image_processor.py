import cv2
import numpy as np
import tensorflow as tf
import base64

def smart_crop_brain(image):
    """
    Crop the image to focus on the brain region using edge detection.
    Ported from test4.py
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
    h, w = image.shape[:2]
    crop_size = min(h, w) * 0.7
    start_x = int((w - crop_size) // 2)
    start_y = int((h - crop_size) // 2)
    return image[start_y:start_y+int(crop_size), start_x:start_x+int(crop_size)]

def preprocess_image(image):
    """
    Preprocess image for model prediction:
    1. Smart crop
    2. Resize to 240x240
    3. Convert to RGB
    4. Normalize to [0, 1]
    5. Add batch dimension
    """
    # Step 1: Crop brain region
    cropped_brain = smart_crop_brain(image)
    
    # Step 2: Resize to 240x240
    resized_image = cv2.resize(cropped_brain, (240, 240))
    
    # Step 3: Convert to RGB
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    
    # Step 4: Normalize to [0, 1]
    normalized_image = rgb_image / 255.0
    
    # Step 5: Add batch dimension
    final_image = np.expand_dims(normalized_image, axis=0)
    
    return final_image, normalized_image

def calculate_histogram(image):
    """
    Calculate pixel intensity histogram for each channel
    """
    # Image is in [0, 1] range, convert to [0, 255] for histogram
    img_uint8 = (image * 255).astype(np.uint8)
    
    hist_data = []
    colors = ('r', 'g', 'b')
    
    for i, color in enumerate(colors):
        hist = cv2.calcHist([img_uint8], [i], None, [256], [0, 256])
        hist_data.append({
            "name": color.upper(),
            "data": hist.flatten().tolist()
        })
        
    return hist_data

def encode_image_to_base64(image):
    """
    Convert numpy image to base64 string
    """
    # Convert to BGR for encoding (if it was RGB)
    if image.max() <= 1.0:
        image = (image * 255).astype(np.uint8)
        
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.png', image_bgr)
    return base64.b64encode(buffer).decode('utf-8')

def calculate_metrics(image):
    """
    Calculate advanced image metrics: Entropy, Contrast, SNR
    """
    # Convert to grayscale for metrics
    gray = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    
    # 1. Entropy (Texture/Complexity)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist.ravel() / hist.sum()
    logs = np.log2(hist + 1e-7)
    entropy = -np.sum(hist * logs)
    
    # 2. Contrast (Standard Deviation of pixel intensities)
    contrast = gray.std()
    
    # 3. SNR (Signal-to-Noise Ratio)
    # Simple approximation: Mean / StdDev
    mean = gray.mean()
    snr = mean / (contrast + 1e-7)
    
    return {
        "entropy": float(entropy),
        "contrast": float(contrast),
        "snr": float(snr)
    }
