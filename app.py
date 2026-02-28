
from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

# allow configuring the frontend origin via env var (e.g. https://your-vercel-app.vercel.app)
frontend_origin = os.environ.get("FRONTEND_ORIGIN", "*")
CORS(app, resources={r"/*": {"origins": frontend_origin}})

# 🔹 Set Tesseract path (CHANGE if different on your PC)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔹 Upload folder setup
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# =========================
# 🧠 INGREDIENT DATABASE
# =========================

# 🔴 COSMETIC INDICATORS
COSMETIC_INDICATORS = [
    "water", "aqua", "glycerin", "cetyl alcohol", "cetearyl alcohol",
    "stearic acid", "glyceryl stearate", "phenoxyethanol", "methylparaben",
    "propylparaben", "butylparaben", "ethylparaben", "benzyl alcohol",
    "sodium hydroxide", "citric acid", "potassium sorbate", "sodium benzoate",
    "fragrance", "parfum", "essential oil", "limonene", "linalool",
    "hyaluronic acid", "aloe vera", "vitamin e", "retinol", "niacinamide",
    "salicylic acid", "glycolic acid", "benzoyl peroxide", "silica",
    "mica", "iron oxides", "titanium dioxide", "zinc oxide", "talc",
    "wax", "lanolin", "jojoba oil", "argan oil", "coconut oil",
    "shea butter", "emulsifier", "stabilizer", "preservative",
    "humectant", "occlusive", "emollient", "surfactant",
    "face", "skin", "hair", "cosmetic", "beauty", "moisturizer",
    "sunscreen", "spf", "lotion", "cream", "serum", "mask",
    "shampoo", "conditioner", "gel", "spray", "cologne", "perfume",
    "makeup", "foundation", "concealer", "powder", "blush", "lipstick"
]

# 🟢 FOOD PRODUCT INDICATORS
FOOD_INDICATORS = [
    "calorie", "protein", "carbohydrate", "carbs", "fat", "sodium",
    "potassium", "fiber", "sugar", "water", "serving", "serving size",
    "nutrition", "nutritional", "value", "per 100g", "contains",
    "ingredients", "energy", "kcal", "kj", "vegan", "vegetarian",
    "gluten", "dairy", "nut", "allergen", "manufactured", "best before",
    "expiry", "batch", "made in", "product of", "net weight",
    "flour", "oil", "butter", "milk", "cheese", "yogurt", "eggs",
    "meat", "chicken", "fish", "salt", "spice", "herb", "seasoning",
    "food", "edible", "snack", "drink", "juice", "tea", "coffee",
    "chocolate", "candy", "biscuit", "bread", "cereal", "pasta",
    "rice", "bean", "lentil", "nut", "seed", "fruit", "vegetable"
]

HIGH_RISK = [
    # 🔴 Sugars
    "sugar", "glucose syrup", "high fructose corn syrup", "corn syrup",
    "maltose", "dextrose", "fructose", "sucrose", "invert sugar",
    "liquid glucose",

    # 🔴 Refined carbs
    "white flour", "maida", "refined wheat flour", "corn starch",
    "modified starch",

    # 🔴 Soft drink chemicals
    "phosphoric acid", "caramel color", "caffeine", "artificial flavors",
    "natural flavors", "aspartame", "acesulfame potassium", "sucralose",

    # 🔴 Unhealthy fats
    "hydrogenated oil", "partially hydrogenated oil", "trans fat",
    "vegetable shortening", "palm oil", "margarine",

    # 🔴 Preservatives
    "sodium benzoate", "potassium sorbate", "calcium propionate",
    "nitrates", "nitrites",

    # 🔴 Flavor enhancers
    "monosodium glutamate", "msg", "disodium inosinate", "disodium guanylate",

    # 🔴 Processed fast food additives
    "emulsifier", "stabilizer", "thickener", "artificial color",
    "synthetic color",
]

MODERATE_RISK = [
    "artificial sweetener", "palm oil", "refined vegetable oil"
]

GOOD_INGREDIENTS = [
    "whole wheat", "oats", "millets", "almond flour", "seeds",
    "stevia", "high fiber"
]


# =========================
# 📊 PRODUCT TYPE DETECTION
# =========================

def detect_product_type(text):
    """Detect if product is cosmetic or food"""
    text_lower = text.lower()
    
    cosmetic_count = sum(1 for item in COSMETIC_INDICATORS if item in text_lower)
    food_count = sum(1 for item in FOOD_INDICATORS if item in text_lower)
    
    if cosmetic_count > food_count and cosmetic_count > 3:
        return "cosmetic"
    else:
        return "food"


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

    # Detect product type
    product_type = detect_product_type(extracted_text)

    # If cosmetic product
    if product_type == "cosmetic":
        return jsonify({
            "extracted_text": extracted_text,
            "product_type": "cosmetic",
            "score": "N/A",
            "risk": "Cosmetic Product",
            "message": "⚠️ This appears to be a cosmetic product",
            "suggestion": "ScanIQ is primarily designed for analyzing food and dietary products for PCOS/PCOD management. For cosmetic safety concerns, please consult dermatological resources or your dermatologist.",
            "note": "Cosmetic analysis feature coming soon!"
        })

    # If food product - perform PCOS analysis
    score, high, moderate, good = calculate_score(extracted_text)
    risk_label, message = classify_risk(score)
    suggestion = generate_suggestions(high)

    return jsonify({
        "extracted_text": extracted_text,
        "product_type": "food",
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
    # Render sets $PORT; fall back to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV", "").lower() != "production"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)