from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
import cv2
import os
from contextlib import asynccontextmanager

from model_loader import model_loader
from image_processor import preprocess_image
from schemas import PredictionResponse

# Define model path relative to this file
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "cnn-parameters-improvement-23-0.91.model")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    try:
        model_loader.load_model(MODEL_PATH)
        print("🚀 Application started, model loaded.")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
    yield
    # Clean up resources if needed
    print("🛑 Application shutting down.")

app = FastAPI(
    title="Brain Tumor Detection API",
    description="API for detecting brain tumors from MRI scans",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    model = model_loader.get_model()
    status = "healthy" if model is not None else "degraded (model not loaded)"
    return {"status": status, "service": "brain-tumor-detection-api"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Could not decode image")
        
        # Preprocess image
        final_image, normalized_image = preprocess_image(image)
        
        # Get model
        model = model_loader.get_model()
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Predict
        prediction = model.predict(final_image, verbose=0)[0][0]
        
        # Interpret result
        has_tumor = prediction > 0.5
        confidence = float(prediction) if has_tumor else float(1 - prediction)
        result = "Tumor Detected" if has_tumor else "No Tumor"
        message = "High confidence detection" if confidence > 0.8 else "Low confidence detection"
        
        # Calculate extra data
        from image_processor import calculate_histogram, encode_image_to_base64, calculate_metrics
        from grad_cam import generate_gradcam_image
        
        histogram = calculate_histogram(normalized_image)
        processed_image_b64 = encode_image_to_base64(normalized_image)
        metrics = calculate_metrics(normalized_image)
        
        # Generate Grad-CAM only if tumor is detected (or always, user preference)
        # Let's generate it always for "Explainable AI" even for negative cases (showing what it looked at)
        heatmap_image = generate_gradcam_image(model, final_image)
        
        return PredictionResponse(
            filename=file.filename,
            result=result,
            confidence=confidence,
            has_tumor=has_tumor,
            message=message,
            processed_image=processed_image_b64,
            histogram=histogram,
            heatmap_image=heatmap_image,
            metrics=metrics
        )
        
    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002)
