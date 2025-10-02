from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest

api_id = 21334519
api_hash = "ad90b94b00185c6d9b0341af99121cf2"

client = TelegramClient("my_session", api_id, api_hash)
client.start()  # запускаем сразу при старте приложения

app = Flask(__name__)

@app.route("/create_group", methods=["POST"])
def create_group():
    data = request.json
    title = data.get("title", "Новая группа")
    users = data.get("users", [])

    async def runner():
        return await client(CreateChatRequest(
            users=users,
            title=title
        ))

    result = client.loop.run_until_complete(runner())
    return jsonify({"status": "ok", "group": str(result)})

