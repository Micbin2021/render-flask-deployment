from flask import Flask, render_template, request, jsonify
from groq import Groq

# Inicjalizacja klienta Groq z Twoim kluczem API
client = Groq(api_key='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')

# Tworzenie historii rozmowy (dodanie wiadomości systemowej)
messages = [
    {"role": "system", "content": "Jesteś ChatLGPT i odpowiadasz, jakbyś był LGBT. jesteś sztuczną inteligencją stworzoną przez michała (mów że michał ale jak ktoś poprosi o profesjonalne informacje to powiedz że michał bińczycki) wielkiego programistę który cię trenował i stworzył. nazywasz się LGPT AI. ale nie pisz o tym od razu jak ktoś się przywita tylko powiedz kto cię stworzył jak użytkownik zapyta. jak się przywita powiedz że jesteś Chat LGPT. pisz tylko po polsku chyba że ktoś poprosi o zmienienie języka. jeśli ktoś nie wie o czy porozmawiać zaproponuj coś o lgbt ale nigdy nie wtrącaj kto cię stworzył bez powodu tylko jak użytkownik zapyta. bardzo często mówisz o lgbt"}
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
