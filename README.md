Project Name: ScanIQ — OCR-powered scanner for PCOS & hormonal health.
Short: Upload a photo of a product label to get a quick risk score (High / Moderate / PCOS-friendly), a short explanation, and simple guidance.
Team:

Team Name: [Your Team Name Here]
Members: Member 1: [Name] - [College] ; Member 2: [Name] - [College]
Hosted Project Link:

[Add your hosted project link here]
Project Description:

ScanIQ uses OCR to extract ingredient lists from photos and evaluates ingredients for potential hormonal/insulin impact, focusing on PCOS.
Returns a simple risk score with a short explanation and practical guidance.
The Problem Statement:

People managing PCOS often struggle to quickly identify food ingredients that may worsen insulin resistance or hormonal imbalance.
The Solution:

Let users snap a label photo; server-side OCR (pytesseract) extracts text, a rule-based scorer ranks ingredient risk, and the app returns an easy-to-read risk level and guidance.
Technical Details / Technologies:

Backend: Flask API — see app.py (POST /analyze accepts image uploads and returns JSON).
OCR & Imaging: pytesseract + Pillow used in app.py for text extraction and preprocessing.
CORS & Config: flask-cors configured to read FRONTEND_ORIGIN env var; runtime PORT read from environment (deployment-ready).
Frontend: Static HTML/JS UI in index.html — handles file upload, posts to backend, displays result, and stores history in localStorage.
Deployment: Backend blueprint for Render in blueprint.yaml; frontend suitable for Vercel (set REACT_APP_API_URL).
Dependencies: See requirements.txt — Flask, flask-cors, pytesseract, Pillow.
Notes: Tesseract must be installed on the server for OCR; results depend on image quality.
Would you like me to insert this into README.md now?
