from fastapi import FastAPI

app = FastAPI(title="AI Voice Detection API")

@app.get("/health")
def health_check():
    return {"status": "ok"}
from fastapi import FastAPI
from pydantic import BaseModel
import random
import base64

app = FastAPI(title="AI Voice Detection API")

# --------- Health endpoint ---------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# --------- Request & Response Schema ---------
class VoiceRequest(BaseModel):
    audio_base64: str
    language: str  # 'ta', 'en', 'hi', 'ml', 'te'

class VoiceResponse(BaseModel):
    classification: str
    confidence: float
    language: str

# --------- Dummy /detect endpoint ---------
@app.post("/v1/voice/detect", response_model=VoiceResponse)
def detect_voice(request: VoiceRequest):
    # Decode Base64 just to check validity (won't process audio here)
    try:
        audio_bytes = base64.b64decode(request.audio_base64)
        if len(audio_bytes) == 0:
            raise ValueError("Empty audio")
    except Exception:
        return {"classification": "ERROR", "confidence": 0.0, "language": request.language}

    # Dummy AI/Human prediction
    classification = random.choice(["AI_GENERATED", "HUMAN"])
    confidence = round(random.uniform(0.5, 0.99), 3)  # dummy confidence

    return {
        "classification": classification,
        "confidence": confidence,
        "language": request.language
    }

