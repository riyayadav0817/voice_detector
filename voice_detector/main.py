from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import random, base64

API_KEY = "my-secret-key" 

app = FastAPI(title="AI Voice Detection API")

class VoiceRequest(BaseModel):
    audio_base64: str
    language: str

class VoiceResponse(BaseModel):
    classification: str
    confidence: float
    language: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/v1/voice/detect", response_model=VoiceResponse)
def detect_voice(request: VoiceRequest, x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        audio_bytes = base64.b64decode(request.audio_base64)
        if len(audio_bytes) == 0:
            raise ValueError("Empty audio")
    except Exception:
        return {"classification": "ERROR", "confidence": 0.0, "language": request.language}

    classification = random.choice(["AI_GENERATED", "HUMAN"])
    confidence = round(random.uniform(0.5, 0.99), 3)

    return {"classification": classification, "confidence": confidence, "language": request.language}
