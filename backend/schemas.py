from pydantic import BaseModel

class PredictionResponse(BaseModel):
    filename: str
    result: str
    confidence: float
    has_tumor: bool
    message: str
    processed_image: str  # Base64 encoded image
    heatmap_image: str | None = None # Base64 encoded Grad-CAM overlay
    histogram: list       # List of histogram data objects
    metrics: dict | None = None # Dictionary of advanced metrics
