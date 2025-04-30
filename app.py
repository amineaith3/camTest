import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai
import base64

load_dotenv()
openai.api_key = os.getenv("OPENAI_TOKEN")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=["POST"])
def analyze_image():
    data = request.json
    image_data = data.get("image")  # base64 string

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "What do you see in this image?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
                ]}
            ],
            max_tokens=500
        )

        result = response.choices[0].message.content
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
