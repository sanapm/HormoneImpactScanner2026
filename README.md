Project Name: ScanIQ 

OCR-powered scanner for PCOS & hormonal health.

<img width="957" height="667" alt="image" src="https://github.com/user-attachments/assets/7af5903f-ed4c-460a-9cc7-af5faf32f200" />

<img width="630" height="710" alt="image" src="https://github.com/user-attachments/assets/f27d4d44-ea44-48e5-aac2-ffbc4dcd9617" />


Team:

Team Name: [SheByte]
Members: Member 1: [Sana P M] - [Model Engineering College] 
Member 2: [Diya Ferose T T] - [Model Engineering College]


Hosted Project Link:

[https://hormone-impact-scanner2026.vercel.app/]


Project Description:

ScanIQ uses OCR to extract ingredient lists from photos and evaluates ingredients for potential hormonal/insulin impact, focusing on PCOS.
Returns a simple risk score with a short explanation and practical guidance.



The Problem Statement:

People managing PCOS often struggle to quickly identify food ingredients that may worsen insulin resistance or hormonal imbalance.


The Solution:

Let users snap a label photo; server-side OCR (pytesseract) extracts text, a rule-based scorer ranks ingredient risk, and the app returns an easy-to-read risk level and guidance.
Technical Details / Technologies:

Backend:

Flask API — see app.py (POST /analyze accepts image uploads and returns JSON).
OCR & Imaging: pytesseract + Pillow used in app.py for text extraction and preprocessing.
CORS & Config: flask-cors configured to read FRONTEND_ORIGIN env var; runtime PORT read from environment (deployment-ready).


Frontend:

Static HTML/JS UI in index.html — handles file upload, posts to backend, displays result, and stores history in localStorage.
Deployment: Backend blueprint for Render in blueprint.yaml; frontend suitable for Vercel (set REACT_APP_API_URL).
Dependencies: See requirements.txt — Flask, flask-cors, pytesseract, Pillow.
Notes: Tesseract must be installed on the server for OCR; results depend on image quality.
Would you like me to insert this into README.md now?
