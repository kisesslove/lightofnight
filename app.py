import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

load_dotenv() # Загружает переменные из .env файла

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"

app = Flask(__name__)

def generate_llm_response(query):
    client = OpenAI(
        base_url=OPENROUTER_API_BASE,
        api_key=OPENROUTER_API_KEY, # Явно передаем ключ OpenRouter
    )

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct", # Используем выбранную модель от Meta Llama 3.3
            messages=[{"role": "user", "content": query}],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при запросе к OpenRouter: {e}")
        print(f"DEBUG: Full error from OpenRouter: {e}") # Добавлена отладочная строка
        return "Извините, у меня возникли проблемы с генерацией ответа."



def chat_response(user_input):
    user_input_lower = user_input.lower()

    if "кто тебя создал" in user_input_lower or "кто твой создатель" in user_input_lower:
        return "меня создал о великий: kisesslove"
    else:
        # Теперь lightofnight отвечает на общие вопросы через имитацию веб-поиска
        return generate_llm_response(user_input)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': 'Сообщение не найдено'}), 400
    
    response = chat_response(user_message)
    return jsonify({'response': response, 'bot_name': 'lightofnight'})

if __name__ == '__main__':
    app.run(debug=True)

