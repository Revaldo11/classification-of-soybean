from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from io import BytesIO
from PIL import Image
from src.adapters.ml_model import MLModelAdapter
from src.use_cases.predict import PredictSoybeanUseCase

app = FastAPI(title="Soybean Classification API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    ml_adapter = MLModelAdapter(model_path="best_model_skenario3.keras", mapping_path="class_mapping.csv")
    predict_use_case = PredictSoybeanUseCase(ml_adapter)
except Exception as e:
    print(f"Error loading model: {e}")
    predict_use_case = None

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/api/status")
def get_status():
    if predict_use_case is not None:
        return {"status": "ready", "message": "Model is loaded and ready"}
    else:
        return {"status": "error", "message": "Model failed to load"}

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
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
