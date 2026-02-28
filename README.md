Project Name: ScanIQ 

OCR-powered scanner for PCOS & hormonal health.

<img width="957" height="667" alt="image" src="https://github.com/user-attachments/assets/7af5903f-ed4c-460a-9cc7-af5faf32f200" />



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

Technical Details — Technologies / Components Used

Languages used: Python (backend), JavaScript (frontend), HTML/CSS (UI)
Frameworks used: Flask (backend web framework; templating via Flask/Jinja2)
Libraries used: Flask-CORS, pytesseract, Pillow (PIL) — plus standard browser APIs (Fetch, localStorage)
Tools & Platform: Git / GitHub, VS Code (dev), Tesseract OCR (system dependency), Render (backend hosting), Vercel (frontend hosting)
Files of interest: app.py, requirements.txt, blueprint.yaml, index.html


 Features:

 
- Image OCR: upload product label photos and extract ingredient text.
- Product classification: identify food vs. cosmetic and handle accordingly.
- Risk scoring: analyze ingredients against PCOS/hormonal risk rules.
- Guidance & history: display color‑coded results, suggestions, and save past scans.
- Extensible database: add new ingredients or dietary rules easily.

 Installation:

 
```bash
# clone/fetch repository
pip install -r [requirements.txt](http://_vscodecontentref_/0)
# ensure Tesseract OCR is installed on your system and the path is set in [app.py](http://_vscodecontentref_/1)
