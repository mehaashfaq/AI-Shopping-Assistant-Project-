# AI-Shopping-Assistant-Project-
# 🛍 AI Shopping Assistant (Image → Product Search System)

## 📌 Overview
This project is an AI-powered web application that allows users to upload an image, extract meaningful captions using computer vision, and automatically search for similar products online. It then ranks results using AI-based similarity scoring and estimates product reliability.

The system combines Computer Vision, Natural Language Processing, and Web Search APIs to simulate a real-world intelligent shopping assistant.

---

## 🚀 Features
- Image captioning using BLIP (Transformer-based AI model)
- Keyword extraction from generated captions
- Web product search using SerpAPI (Google search API)
- AI-based similarity matching using Sentence Transformers
- Product ranking system
- Scam/risk estimation based on similarity score
- Flask-based web interface

---

## 🧠 How It Works
1. User uploads an image  
2. BLIP model generates a text description of the image  
3. Keywords are extracted from the caption  
4. SerpAPI searches for related products online  
5. Sentence Transformer compares similarity between caption and product titles  
6. System ranks products and selects the best match  
7. Results are displayed in a web interface  

---

## 🛠 Tech Stack
- Python
- Flask
- Hugging Face Transformers (BLIP Model)
- Sentence-Transformers
- SerpAPI
- HTML / CSS (basic frontend)

---


---

## ⚙️ Installation & Setup

### 1. Clone the repository
bash
git clone https://github.com/your-username/ai-shopping-assistant.git
cd ai-shopping-assistant

2. Install dependencies
pip install -r requirements.txt

3. Add API Key (IMPORTANT)

This project uses SerpAPI.
You must create your own API key here:

👉 https://serpapi.com/

Then set environment variable:

Windows (CMD)
set SERP_API_KEY=your_api_key_here
Mac/Linux
export SERP_API_KEY=your_api_key_here
4. Run the application
python app.py

Open in browser:

http://127.0.0.1:5000/

