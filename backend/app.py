# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import save_capsule, get_capsules, categorize_capsule, remove_capsule
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)
CORS(app)

@app.route("/api/capsules", methods=["GET"])
def list_capsules():
    capsules = get_capsules()
    return jsonify(capsules)

@app.route("/api/capsules", methods=["POST"])
def create_capsule():
    data = request.get_json()
    title = data.get("title")
    message = data.get("message")
    future_date = data.get("future_date")

    try:
        from utils import get_capsules
        capsules = get_capsules()
        category = categorize_capsule(message, capsules)
    except Exception as e:
        print("Categorization failed:", e)
        category = "Other"
    capsule = save_capsule(title, message, future_date, category)
    return jsonify({"message": "Capsule saved successfully", "capsule": capsule, "category": category})

@app.route("/api/capsules/<int:capsule_id>", methods=["DELETE"])
def delete_capsule(capsule_id):
    success = remove_capsule(capsule_id)
    if success:
        return jsonify({"message": "Capsule deleted successfully"})
    else:
        return jsonify({"error": "Capsule not found"}), 404
    
# AI Chat Endpoint
@app.route("/api/ai-chat", methods=["POST"])
def ai_chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
    capsules = data.get("capsules", [])

    # Combine all past messages into context
    context = "\n".join([f"- {c['message']}" for c in capsules])
    system_prompt = f"""
You are a compassionate self-therapist AI. 
You have access to the user's past time capsules:
{context}

When the user writes a prompt, provide guidance, encouragement, and actionable advice based on the user's past capsules. Be empathetic and motivational.
Respond in a friendly, supportive way.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        answer = response.choices[0].message["content"].strip()
        return jsonify({"response": answer})
    except Exception as e:
        print("AI Chat Error:", e)
        return jsonify({"response": "Sorry, something went wrong with AI."}), 500
    
if __name__ == "__main__":
    app.run(debug=True)

