# =========================
# Code Cell
# =========================
# =========================

# Imports

# =========================

from flask import Flask, render_template_string, request

from PIL import Image

from transformers import BlipProcessor, BlipForConditionalGeneration

from sentence_transformers import SentenceTransformer, util

import requests, os

import threading

import nest_asyncio



# =========================

# Fix for Jupyter + Flask

# =========================

nest_asyncio.apply()



# =========================

# API Keys and Models

# =========================

SERP_API_KEY = " Your SERP_API_KEY"

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)



# Load models (takes time)

print("Loading models...")

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")

blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

sim_model = SentenceTransformer('all-MiniLM-L6-v2')

print("Models loaded!")



# =========================

# Flask App

# =========================

app = Flask(__name__)



# =========================

# AI + Search Function

# =========================

def analyze_image_and_search(image_path):

    # BLIP Caption

    image = Image.open(image_path)

    inputs = processor(image, return_tensors="pt")

    out = blip_model.generate(**inputs)

    caption = processor.decode(out[0], skip_special_tokens=True)



    # Keywords

    keywords = [w for w in caption.replace(",", "").split() if len(w) > 3]



    # SerpAPI Search

    url = "https://serpapi.com/search.json"

    params = {

        "engine": "google",

        "q": caption + " site:amazon.com OR site:daraz.pk",

        "api_key": SERP_API_KEY

    }

    response = requests.get(url, params=params).json()

    products = []

    if "organic_results" in response:

        for r in response["organic_results"]:

            title = r.get("title","")

            link = r.get("link","")

            snippet = r.get("snippet","")

            price = 0

            for word in snippet.replace(",","").split():

                if word.startswith("$") or word.isdigit():

                    try:

                        price = int(word.replace("$",""))

                        break

                    except: continue

            products.append({"title":title,"link":link,"price":price})



    # Match Score & Scam Risk

    for p in products:

        emb1 = sim_model.encode(caption, convert_to_tensor=True)

        emb2 = sim_model.encode(p["title"], convert_to_tensor=True)

        p["match_score"] = float(util.cos_sim(emb1, emb2))

        p["scam_risk_%"] = 30 if p["match_score"] < 0.5 else 10



    # Best Buy

    best = sorted(products, key=lambda x: (x["scam_risk_%"], -x["price"]))[0] if products else {}

    return {"caption": caption, "keywords": keywords, "products": products, "best_buy": best}



# =========================

# Flask Route

# =========================

HTML_TEMPLATE = """

<!DOCTYPE html>

<html>

<head>

    <title>AI Shopping Assistant</title>

    <style>

        body { font-family: Arial; background: #f0f8ff; text-align: center; padding: 30px; }

        .container { background: white; padding: 20px; border-radius: 15px; display: inline-block; }

        h1 { color: #007ACC; }

        input[type=file] { margin: 20px 0; }

        .product { margin: 10px 0; }

        .best { color: green; font-weight: bold; }

        button { background-color: #007ACC; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; }

        button:hover { background-color: #005a99; }

    </style>

</head>

<body>

<div class="container">

    <h1>🛍 AI Shopping Assistant</h1>

    <form method="POST" enctype="multipart/form-data">

        <input type="file" name="image" accept="image/*" required>

        <br>

        <button type="submit">Analyze & Search</button>

    </form>

    {% if result %}

        <h2>🖼 Caption:</h2>

        <p>{{ result['caption'] }}</p>

        <h3>🔑 Keywords:</h3>

        <p>{{ result['keywords'] | join(', ') }}</p>

        <h3>🛍 Products Found:</h3>

        <ul>

        {% for p in result['products'] %}

            <li class="product">

                <a href="{{ p['link'] }}" target="_blank">{{ p['title'] }}</a> - Price: {{ p['price'] }} - Scam Risk: {{ p['scam_risk_%'] }}%

            </li>

        {% endfor %}

        </ul>

        {% if result['best_buy'] %}

            <h3 class="best">✅ Best Buy Recommendation:</h3>

            <p>

                <a href="{{ result['best_buy']['link'] }}" target="_blank">{{ result['best_buy']['title'] }}</a> - Price: {{ result['best_buy']['price'] }}

            </p>

        {% endif %}

    {% endif %}

</div>

</body>

</html>

"""



@app.route("/", methods=["GET", "POST"])

def index():

    result = None

    if request.method == "POST":

        if "image" not in request.files:

            return render_template_string(HTML_TEMPLATE, result=None, error="No file uploaded.")

        file = request.files["image"]

        if file.filename == "":

            return render_template_string(HTML_TEMPLATE, result=None, error="No file selected.")

        file_path = os.path.join(UPLOAD_DIR, file.filename)

        file.save(file_path)

        result = analyze_image_and_search(file_path)

    return render_template_string(HTML_TEMPLATE, result=result)



# =========================

# Run Flask in a Thread

# =========================

def run_app():

    app.run(port=5000)



threading.Thread(target=run_app).start()

print("Flask app running at http://127.0.0.1:5000/")



# =========================
# Code Cell
# =========================

