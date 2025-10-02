from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, ToggleForumRequest
from telethon.tl.functions.forums import CreateForumTopicRequest

# 🔑 Данные из my.telegram.org
api_id = 21334519
api_hash = "ad90b94b00185c6d9b0341af99121cf2"

# Создаём клиент
client = TelegramClient("my_session", api_id, api_hash)
app = Flask(__name__)

@app.route("/create_group", methods=["POST"])
def create_group():
    try:
        data = request.json
        title = data.get("title", "Новая супергруппа")
        topics = data.get("topics", ["Общий чат", "Вопросы", "Новости"])

        async def runner():
            # 1. Создаём супергруппу
            created = await client(CreateChannelRequest(
                title=title,
                about="Автоматически созданная группа",
                megagroup=True
            ))
            channel = created.chats[0]

            # 2. Включаем режим форума (топики)
            await client(ToggleForumRequest(
                channel=channel,
                enabled=True
            ))

            # 3. Создаём топики из списка
            created_topics = []
            for name in topics:
                topic = await client(CreateForumTopicRequest(
                    channel=channel,
                    title=name,
                    icon_color=7322096  # можно менять цвет
                ))
                created_topics.append(name)

            return {
                "chat_id": channel.id,
                "title": title,
                "topics": created_topics
            }

        with client:
            result = client.loop.run_until_complete(runner())

        return jsonify({"status": "ok", "group": result})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
