from flask import Flask, render_template, request
import requests
# import openai

app = Flask(__name__)

# API endpoint for ChatGPT
CHATGPT_API_URL = "https://api.openai.com/v1/chat/completions"

# Your OpenAI ChatGPT API key
API_KEY = "your api key"


@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        condition = request.form.get("condition")
        severity = request.form.get("severity")
        user_message = request.form.get("message")

        # Generate a chat response using ChatGPT API
        response = generate_chat_response(condition, severity, user_message)

        return render_template("index.html", response=response)

    return render_template("index.html")


def generate_chat_response(condition, severity, message):
    # Create the payload for the ChatGPT API request
    payload = {
        
        "model":"text-davinci-002",
        "messages": [
            {"role": "system", "content": f"Condition: {condition}"},
            {"role": "system", "content": f"Severity: {severity}"},
            {"role": "user", "content": message},
        ],
        "max_tokens": 50,  # Adjust the max tokens based on your desired response length
        
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    # Send the request to the ChatGPT API
    response = requests.post(CHATGPT_API_URL, json=payload, headers=headers)

    # Extract the generated chat response
    chat_response = response.json() #["choices"][0]["message"]["content"]
    print(chat_response)
    return chat_response


if __name__ == "__main__":
    app.run(debug=True)
