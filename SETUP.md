# NeuroScan AI - Setup & Installation Guide

## Prerequisites
- **Python 3.8+** (Tested with 3.12)
- **Node.js 16+** & **npm**
- **Git**

## 1. Clone the Repository
```bash
git clone https://github.com/Aryan-Shan/NeuroScan-AI.git
cd NeuroScan-AI
```

## 2. Backend Setup
The backend is built with FastAPI and TensorFlow.

### Create Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
**Important**: You must install `h5py` separately or ensure it is included, as it is critical for loading the Keras model.
```bash
cd backend
pip install -r requirements.txt
pip install h5py
```

### Model Setup
Place your trained model file `cnn-parameters-improvement-23-0.91.model` in the `backend/models/` directory.
*Note: The model file is excluded from git by default due to size.*

### Run the Server
The backend runs on port **8002** by default.
```bash
python main.py
```
You should see: `Uvicorn running on http://0.0.0.0:8002`

## 3. Frontend Setup
The frontend is built with React, Vite, and TailwindCSS.

### Install Dependencies
```bash
cd frontend
npm install
```

### Run the Application
```bash
npm run dev
```
The application will start at `http://localhost:5173`.

## 4. Usage
1. Open `http://localhost:5173` in your browser.
2. Drag and drop a brain MRI scan image into the upload zone.
3. View the prediction results, confidence score, and pixel intensity analysis.
4. Download the detailed PDF report if needed.

## Troubleshooting
- **"Model not loaded"**: Ensure the model file is in the correct path and `h5py` is installed.
- **"Address already in use"**: The backend uses port 8002. Ensure no other service is using this port.
- **Frontend API Error**: Check `frontend/src/utils/api.ts` and ensure `baseURL` matches the backend URL (default `http://localhost:8002`).
