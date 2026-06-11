from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from io import BytesIO
from PIL import Image
from threading import Lock, Thread

app = FastAPI(title="Soybean Classification API")

model_state = {
    "status": "loading",
    "message": "Model sedang dimuat",
    "predict_use_case": None,
}
model_state_lock = Lock()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_model_background():
    try:
        from src.adapters.ml_model import MLModelAdapter
        from src.use_cases.predict import PredictSoybeanUseCase

        ml_adapter = MLModelAdapter(
            model_path="best_model_skenario3.keras",
            mapping_path="class_mapping.csv"
        )
        predict_use_case = PredictSoybeanUseCase(ml_adapter)

        with model_state_lock:
            model_state["status"] = "ready"
            model_state["message"] = "Model berhasil dimuat"
            model_state["predict_use_case"] = predict_use_case
    except Exception as e:
        print(f"Error loading model: {e}")
        with model_state_lock:
            model_state["status"] = "error"
            model_state["message"] = str(e)
            model_state["predict_use_case"] = None


Thread(target=load_model_background, daemon=True).start()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/api/status")
def get_status():
    with model_state_lock:
        return {
            "status": model_state["status"],
            "message": model_state["message"],
        }

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    with model_state_lock:
        status = model_state["status"]
        predict_use_case = model_state["predict_use_case"]

    if status == "loading":
        raise HTTPException(status_code=503, detail="Model masih dimuat. Silakan coba beberapa saat lagi.")

    if not predict_use_case:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
        
    allowed_types = ["image/png", "image/jpeg", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Format file tidak didukung. Gunakan PNG, JPG, atau WEBP.")
        
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        
        # Execute use case
        result = predict_use_case.execute(image)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
