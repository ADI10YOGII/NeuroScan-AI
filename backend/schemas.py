from pydantic import BaseModel

class PredictionResponse(BaseModel):
    filename: str
    result: str
    confidence: float
    has_tumor: bool
    message: str
    processed_image: str  # Base64 encoded image
    histogram: list       # List of histogram data objects
