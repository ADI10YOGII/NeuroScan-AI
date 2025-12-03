import requests
import os

def test_backend():
    base_url = "http://localhost:8002"
    
    # 1. Test Health Check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health Check: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"❌ Backend not running or health check failed: {e}")
        return

    # 2. Test Prediction
    image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_images", "Y1.jpg")
    if not os.path.exists(image_path):
        print(f"❌ Test image not found at {image_path}")
        return

    print(f"\nTesting prediction with {image_path}...")
    try:
        with open(image_path, "rb") as f:
            files = {"file": ("Y1.jpg", f, "image/jpeg")}
            response = requests.post(f"{base_url}/predict", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction Successful!")
            print(f"Result: {result['result']}")
            print(f"Confidence: {result['confidence']:.2%}")
            
            if 'processed_image' in result and result['processed_image']:
                print("✅ Processed image returned")
            else:
                print("❌ Processed image MISSING")
                
            if 'histogram' in result and len(result['histogram']) == 3:
                print("✅ Histogram data returned")
            else:
                print("❌ Histogram data MISSING")
                
            if 'heatmap_image' in result and result['heatmap_image']:
                print("✅ Grad-CAM Heatmap returned")
            else:
                print("❌ Grad-CAM Heatmap MISSING")
                
            if 'metrics' in result:
                print(f"✅ Metrics returned: {result['metrics']}")
            else:
                print("❌ Metrics MISSING")
                
        else:
            print(f"❌ Prediction Failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error during prediction request: {e}")

if __name__ == "__main__":
    test_backend()
