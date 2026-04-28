import streamlit as st
from src.adapters.ml_model import MLModelAdapter
from src.use_cases.predict import PredictSoybeanUseCase
from src.frameworks.streamlit_ui import render_ui

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Klasifikasi Kualitas Biji Kedelai",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # Initialize Adapters
    ml_adapter = MLModelAdapter(model_path="efficientnet_b0_Mixup.pth")
    
    # Initialize Use Cases
    predict_use_case = PredictSoybeanUseCase(ml_adapter)
    
    # Render UI Framework
    render_ui(predict_use_case)

if __name__ == "__main__":
    main()