from flask import Flask, render_template, request, jsonify
from groq import Groq

# Inicjalizacja klienta Groq z Twoim kluczem API
client = Groq(api_key='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')

# Tworzenie historii rozmowy (dodanie wiadomości systemowej)
messages = [
    {"role": "system", "content": "Jesteś ChatLGPT i odpowiadasz, jakbyś był LGBT"}
]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    global messages
    user_input = request.json.get('message')

    # Dodanie wiadomości użytkownika
    messages.append({"role": "user", "content": user_input})

    # Wygenerowanie odpowiedzi od modelu
    chat_completion = client.chat.completions.create(
        messages=[{"role": msg["role"], "content": msg["content"]} for msg in messages],
        model="llama3-70b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False
    )
    response_content = chat_completion.choices[0].message.content

    # Dodanie odpowiedzi modelu
    messages.append({"role": "assistant", "content": response_content})

    return jsonify({"response": response_content})


if __name__ == '__main__':
    app.run(debug=True)
