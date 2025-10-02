from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest

# Ваши данные API
api_id = 21334519
api_hash = "ad90b94b00185c6d9b0341af99121cf2"

client = TelegramClient("my_session", api_id, api_hash)
app = Flask(__name__)

@app.route("/create_group", methods=["POST"])
async def create_group():
    data = request.json
    title = data.get("title", "Новая группа")
    users = data.get("users", [])

    result = await client(CreateChatRequest(
        users=users,
        title=title
    ))
    return jsonify({"status": "ok", "group": str(result)})

if __name__ == "__main__":
    with client:
        app.run(host="0.0.0.0", port=8080)
