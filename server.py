from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest

# 🔑 Данные из my.telegram.org
api_id = 21334519
api_hash = "ad90b94b00185c6d9b0341af99121cf2"

# создаём клиент
client = TelegramClient("my_session", api_id, api_hash)
app = Flask(__name__)

@app.route("/create_group", methods=["POST"])
def create_group():
    try:
        data = request.json
        title = data.get("title", "Новая группа")
        users = data.get("users", [])

        # обёртка для асинхронного вызова
        async def runner():
            return await client(CreateChatRequest(
                users=users,
                title=title
            ))

        # запускаем Telethon внутри синхронного Flask
        with client:
            result = client.loop.run_until_complete(runner())

        return jsonify({"status": "ok", "group": str(result)})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Render будет запускать через gunicorn, поэтому main-блок можно не писать
