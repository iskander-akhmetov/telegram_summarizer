# 🤖 Telegram Summarizer Bot (telegram_summarizer)

Tired of scrolling through hundreds of Telegram messages across dozens of groups?  
This project is a **Telegram Summarizer Bot** that automatically collects messages from your groups, summarizes them with AI, and delivers a clean digest straight to your private chat.  

Instead of drowning in noise, you get **clarity, structure, and links back to the original messages**.

---

## ✨ Features

- ✅ Collects messages from multiple Telegram groups.
- ✅ Groups messages by topic (work, study, hobbies, etc.).
- ✅ Summarizes conversations with a local AI model (via [Ollama](https://ollama.com/)).
- ✅ Attaches direct links to original Telegram messages for context.
- ✅ Sends a digest to your private chat or chosen group.
- ✅ Option to mark messages as read after processing.
- ✅ Secure local execution — your data never leaves your machine.

---

## 🛠 Tech Stack

- [Pyrogram](https://docs.pyrogram.org/) — Python framework for Telegram API.  
- [Ollama](https://ollama.com/) — run large language models locally.  
- Python (asyncio, requests) — scripting and glue logic.  
- [python-dotenv](https://pypi.org/project/python-dotenv/) — for managing credentials.  
- [tqdm](https://tqdm.github.io/) — progress bars while fetching messages.  

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/iskander-akhmetov/telegram_summarizer.git
cd telegram_summarizer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root with your Telegram credentials:

```ini
API_ID=your_api_id
API_HASH=your_api_hash
OWNER_ID=your_telegram_user_id
```

👉 To get `API_ID` and `API_HASH`, log in at [my.telegram.org](https://my.telegram.org) → API Development.  
👉 To get your `OWNER_ID`, send `/start` to [@userinfobot](https://t.me/userinfobot).  

---

## ⚙️ Setting up Ollama

Install [Ollama](https://ollama.com/download) and pull the summarization model:

```bash
ollama pull gpt-oss:20b
```

Make sure the Ollama server is running locally (`http://localhost:11434`).  

---

## ▶️ Usage

Run the summarizer normally:

```bash
python Telegram_summarizer.py
```

To list all available groups and chats (to get their IDs):

```bash
python Telegram_summarizer.py --list-groups
```

---

## 📅 Automation

To run the summarizer automatically every day:

- **Linux/macOS** — add a cron job, e.g.:

```bash
0 18 * * * /usr/bin/python3 /path/to/Telegram_summarizer.py
```

- **Windows** — use Task Scheduler to run the script daily at a chosen time.  

---

## 📥 Get the Code

This project is open-source:  
👉 [GitHub Repository – Telegram Summarizer](https://github.com/iskander-akhmetov/telegram_summarizer)

---

## 💖 Support & Donations

If this project saves you time, consider supporting my work:  

- 💖 [Donate via PayPal](https://www.paypal.me/your-username)  

Your support helps me improve this project and keep building more open-source tools like it.  

---

## 📜 License

**Personal Use License**  

This software is free for personal and non-commercial use.  
Commercial use (including integration into products or services, resale, or business usage) requires a separate commercial license.  

For commercial licensing inquiries, please contact:  
📧 [iskander.akhmetov@gmail.com]  

---
