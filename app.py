from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

# 🔹 Set Tesseract path (CHANGE if different on your PC)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔹 Upload folder setup
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# =========================
# 🧠 INGREDIENT DATABASE
# =========================

HIGH_RISK = [
    "sugar", "glucose syrup", "high fructose corn syrup",
    "maltose", "dextrose", "white flour",
    "maida", "corn starch"
]

MODERATE_RISK = [
    "artificial sweetener",
    "palm oil",
    "refined vegetable oil"
]

GOOD_INGREDIENTS = [
    "whole wheat", "oats", "millets",
    "almond flour", "seeds",
    "stevia", "high fiber"
]


# =========================
# 📊 SCORING FUNCTION
# =========================

def calculate_score(text):

    text = text.lower()

    score = 0
    detected_high = []
    detected_moderate = []
    detected_good = []

    for item in HIGH_RISK:
        if item in text:
            score += 2
            detected_high.append(item)

    for item in MODERATE_RISK:
        if item in text:
            score += 1
            detected_moderate.append(item)

    for item in GOOD_INGREDIENTS:
        if item in text:
            score -= 1
            detected_good.append(item)

    return score, detected_high, detected_moderate, detected_good


# =========================
# 🚦 RISK CLASSIFICATION
# =========================

def classify_risk(score):

    if score >= 4:
        return "High Risk", "🔴 May Trigger Insulin Spike"

    elif 2 <= score <= 3:
        return "Moderate Risk", "🟡 Consume in moderation"

    else:
        return "PCOS Friendly", "🟢 Low Hormonal Impact"


# =========================
# 💡 SUGGESTIONS
# =========================

def generate_suggestions(high_detected):

    if len(high_detected) > 0:
        return "Consider switching to high-fiber, whole-grain alternatives."
    else:
        return "This product looks relatively balanced."


# =========================
# 🏠 HOME ROUTE
# =========================

from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# 📸 ANALYZE ROUTE
# =========================

@app.route('/analyze', methods=['POST'])
def analyze():

    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        image = Image.open(filepath)
        extracted_text = pytesseract.image_to_string(image)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    score, high, moderate, good = calculate_score(extracted_text)
    risk_label, message = classify_risk(score)
    suggestion = generate_suggestions(high)

    return jsonify({
        "extracted_text": extracted_text,
        "score": score,
        "risk": risk_label,
        "message": message,
        "high_risk_detected": high,
        "moderate_detected": moderate,
        "good_detected": good,
        "suggestion": suggestion
    })


# =========================
# ▶ RUN SERVER
# =========================

if __name__ == "__main__":
    app.run(debug=True)