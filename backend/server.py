import openai
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path

# Carregar o .env da pasta config na raiz do projeto
dotenv_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(dotenv_path)

# Pegar a chave da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Verificar se a chave foi carregada corretamente
if not OPENAI_API_KEY:
    raise ValueError("❌ A chave da OpenAI não foi encontrada. Verifique o arquivo .env!")

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "API está funcionando!", 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True)

        if not data or "message" not in data:
            return jsonify({"error": "O JSON precisa conter a chave 'message'."}), 400

        user_message = data["message"]

        # Nova forma de chamar a API da OpenAI (openai>=1.0.0)
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Ou "gpt-4" se tiver acesso
            messages=[
                {"role": "system", "content": "Você é um assistente útil."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_response = response.choices[0].message.content

        return jsonify({"reply": bot_response})

    except Exception as e:
        return jsonify({"error": f"Erro ao processar IA: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
