# Brain Tumor Detection Web App

A modern, AI-powered web application for detecting brain tumors from MRI scans with 91% accuracy.

## 🚀 Features

- **High Accuracy**: Uses a custom CNN model with 91% accuracy.
- **Instant Analysis**: Real-time inference using FastAPI.
- **Smart Preprocessing**: Automatic brain region cropping and image enhancement.
- **Modern UI**: Clean, medical-grade interface built with React and TailwindCSS.
- **Secure**: Privacy-focused design with local processing capability.

## 🛠️ Tech Stack

- **Frontend**: React, Vite, TypeScript, TailwindCSS, Framer Motion
- **Backend**: FastAPI, TensorFlow/Keras, OpenCV
- **Model**: Convolutional Neural Network (CNN)

## 🏁 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```
The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
The web app will be available at `http://localhost:5173`.

## 📝 API Documentation

- **POST /predict**: Upload an image file to get a prediction.
- **GET /health**: Check API health status.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. It is not intended to replace professional medical diagnosis.
