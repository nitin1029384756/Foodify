import openai
import base64
from flask import Flask, render_template, request
import os

openai.api_key = "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"

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def analyze_image(image_path):
    base64_image = encode_image(image_path)

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image and how many calories? Tell me in 15 words."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )

    return response["choices"][0]["message"]["content"]

@app.route('/')
def index():
    return render_template('NewWebsite.html')  # your upload page

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        description = analyze_image(file_path)
        return render_template('result.html', description=description)  # USE TEMPLATE!

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
