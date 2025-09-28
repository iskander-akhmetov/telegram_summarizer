import os
import datetime
import requests
from dotenv import load_dotenv
from pyrogram import Client
from tqdm import tqdm
import argparse

# --- Загрузка конфигурации ---
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "Telegram summarizer"
OWNER_ID = int(os.getenv("OWNER_ID"))

# --- Настройка тем и групп (пример — замените своими) ---
TOPIC_GROUPS = {
    "My Hobby": [
        -100111111111, -100222222222
    ],
    "My English": [
        -100333333333
    ],
    "Personal": [
        -1004444444444
    ],
    "My Business": [
        -1005555555555
    ]
    
}

TOPIC_TARGET_CHAT = {
    "My Hobby": -411111111,
    "My English": -422222222,
    "Personal": OWNER_ID,
    "My Business": -4333333333   
}

TODAY = datetime.date.today().isoformat()
LOG_FILE = f"logs_{TODAY}.txt"
print("Today", TODAY)

# --- Клиент ---
client = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)


def log_event(message: str):
    """Пишем лог в файл текущего дня"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now().isoformat()}] {message}\n")


def summarize_with_ollama(text: str) -> str:
    """Суммаризация через локальную модель Ollama"""
    payload = {
        "model": "gpt-oss:20b",
        "prompt": f"Сделай краткое саммари этих сообщений, если нужно раздели на подтемы, подчеркни то что важно:\n\n{text}",
        "stream": False
    }
    resp = requests.post("http://localhost:11434/api/generate", json=payload)
    resp.raise_for_status()
    return resp.json()["response"]


MAX_LINKS = 30  # максимум ссылок в дайджесте


async def process_topic(app: Client, topic: str, group_ids: list[int], target_chat: int):
    all_texts = []
    links_by_group = {}

    for group_id in tqdm(group_ids, desc=f"Обработка {topic}"):
        chat = await app.get_chat(group_id)
        chat_name = chat.title or f"ID {group_id}"
        links_by_group.setdefault(chat_name, [])

        async for msg in app.get_chat_history(group_id, limit=500):
            if msg.date.date() == datetime.date.today() and msg.text:
                text = str(msg.text or "")
                preview = text[:20].replace("\n", " ")

                # формируем ссылку
                if chat.username:
                    link = f"https://t.me/{chat.username}/{msg.id}"
                else:
                    link = f"https://t.me/c/{str(group_id)[4:]}/{msg.id}"

                all_texts.append(
                    f"[{chat_name}] {msg.from_user.first_name if msg.from_user else 'anon'}: {text}"
                )
                links_by_group[chat_name].append(f"- {preview}... {link}")

        # отмечаем все сообщения в этой группе как прочитанные
        await app.read_chat_history(group_id)

    if not all_texts:
        log_event(f"{topic}: сообщений не найдено.")
        return

    summary = summarize_with_ollama("\n".join(all_texts))

    # собираем блок ссылок
    links_block = []
    total_links = 0
    for chat_name, links in links_by_group.items():
        if not links:
            continue
        links_block.append(f"▶ {chat_name}")
        for l in links:
            if total_links >= MAX_LINKS:
                break
            links_block.append(l)
            total_links += 1
        if total_links >= MAX_LINKS:
            links_block.append(
                f"...и ещё {sum(len(v) for v in links_by_group.values()) - MAX_LINKS} сообщений"
            )
            break

    final_text = (
        f"📌 Дайджест по теме **{topic}** за {TODAY}:\n\n"
        f"{summary}\n\n"
        f"📎 Ссылки на сообщения:\n" + "\n".join(links_block)
    )

    await app.send_message(target_chat, final_text, disable_web_page_preview=True)
    log_event(f"{topic}: собрано {len(all_texts)} сообщений → отправлено в {target_chat}")


async def list_groups(app: Client):
    """
    Выводит список всех чатов (группы, каналы, личные), доступных клиенту.
    """
    print("📋 Доступные чаты:")
    async for dialog in app.get_dialogs():
        chat = dialog.chat
        print(f"- {chat.title or chat.first_name} :: {chat.id}")


async def main(app: Client):
    for topic, groups in TOPIC_GROUPS.items():
        print(f"== Обработка темы: {topic} ==")
        target_chat = TOPIC_TARGET_CHAT.get(topic, OWNER_ID)
        await process_topic(app, topic, groups, target_chat)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telegram Summarizer")
    parser.add_argument("--list-groups", action="store_true", help="Вывести список доступных чатов")
    args = parser.parse_args()

    if args.list_groups:
        client.run(list_groups)
    else:
        client.run(main)
