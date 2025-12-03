import tensorflow as tf
import numpy as np
import cv2
import base64

class GradCAM:
    def __init__(self, model, layer_name=None):
        self.model = model
        self.layer_name = layer_name or self.find_last_conv_layer()
        
        if self.layer_name is None:
            raise ValueError("Could not find a convolutional layer in the model.")
            
        self.grad_model = tf.keras.models.Model(
            inputs=[model.inputs],
            outputs=[model.get_layer(self.layer_name).output, model.output]
        )

    def find_last_conv_layer(self):
        """
        Dynamically find the last Conv2D layer in the model
        """
        for layer in reversed(self.model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                return layer.name
        return None

    def compute_heatmap(self, image, eps=1e-8):
        """
        Compute Grad-CAM heatmap
        """
        with tf.GradientTape() as tape:
            inputs = tf.cast(image, tf.float32)
            (conv_outputs, predictions) = self.grad_model(inputs)
            loss = predictions[:, 0] # Assume binary classification, target class 0 or 1 depending on implementation
            # For this specific model, we want to explain the "Tumor" prediction.
            # If prediction > 0.5 (Tumor), we explain that.
            
        grads = tape.gradient(loss, conv_outputs)
        
        cast_conv_outputs = tf.cast(conv_outputs > 0, "float32")
        cast_grads = tf.cast(grads > 0, "float32")
        guided_grads = cast_conv_outputs * cast_grads * grads
        
        conv_outputs = conv_outputs[0]
        guided_grads = guided_grads[0]
        
        weights = tf.reduce_mean(guided_grads, axis=(0, 1))
        cam = tf.reduce_sum(tf.multiply(weights, conv_outputs), axis=-1)
        
        heatmap = cv2.resize(cam.numpy(), (image.shape[2], image.shape[1]))
        
        heatmap = np.maximum(heatmap, 0)
        heatmap = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min() + eps)
        
        return heatmap

    def overlay_heatmap(self, image, heatmap, alpha=0.4):
        """
        Overlay heatmap on original image and draw bounding box
        """
        # Image is (1, 240, 240, 3) float32 [0,1]
        # Convert to uint8 [0,255]
        img_uint8 = (image[0] * 255).astype(np.uint8)
        img_uint8 = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2BGR)
        
        # Process heatmap
        heatmap_uint8 = (heatmap * 255).astype(np.uint8)
        heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        
        # Overlay
        overlay = cv2.addWeighted(img_uint8, 1 - alpha, heatmap_color, alpha, 0)
        
        # Find Bounding Box from heatmap
        # Threshold the heatmap to get the "hot" region
        _, thresh = cv2.threshold(heatmap_uint8, 100, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest contour
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            
            # Draw bounding box (Green)
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Add label
            cv2.putText(overlay, "AI Focus", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
        return overlay

def generate_gradcam_image(model, image):
    try:
        grad_cam = GradCAM(model)
        heatmap = grad_cam.compute_heatmap(image)
        overlay = grad_cam.overlay_heatmap(image, heatmap)
        
        # Encode to base64
        _, buffer = cv2.imencode('.png', overlay)
        return base64.b64encode(buffer).decode('utf-8')
    except Exception as e:
        print(f"Grad-CAM Error: {e}")
        return None
