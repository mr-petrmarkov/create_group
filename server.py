from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest, ToggleForumRequest
from telethon.tl.functions.forums import CreateForumTopicRequest

# 🔑 Данные из my.telegram.org
api_id = 21334519
api_hash = "ad90b94b00185c6d9b0341af99121cf2"

client = TelegramClient("my_session", api_id, api_hash)
app = Flask(__name__)

@app.route("/create_group", methods=["POST"])
def create_group():
    try:
        data = request.json
        title = data.get("title", "Новая супергруппа")
        users = [str(u).replace("@", "").strip() for u in data.get("users", [])]
        topics = data.get("topics", ["Общий чат", "Вопросы", "Новости"])

        async def runner():
            # 1. Создаём супергруппу
            created = await client(CreateChannelRequest(
                title=title,
                about="Автоматически созданная группа",
                megagroup=True
            ))
            channel = created.chats[0]

            # 2. Добавляем участников (если есть)
            if users:
                try:
                    await client(InviteToChannelRequest(
                        channel=channel,
                        users=users
                    ))
                except Exception as e:
                    print("Ошибка при добавлении участников:", e)

            # 3. Включаем режим форума
            await client(ToggleForumRequest(
                channel=channel,
                enabled=True
            ))

            # 4. Создаём топики
            created_topics = []
            for name in topics:
                try:
                    await client(CreateForumTopicRequest(
                        channel=channel,
                        title=name,
                        icon_color=7322096
                    ))
                    created_topics.append(name)
                except Exception as e:
                    print(f"Ошибка при создании топика {name}:", e)

            return {
                "chat_id": channel.id,
                "title": title,
                "users": users,
                "topics": created_topics
            }

        with client:
            result = client.loop.run_until_complete(runner())

        return jsonify({"status": "ok", "group": result})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

