 🩺 ProductBot — AI-Powered Patient Interaction Bot

**ProductBot** is a Telegram-based bot designed to streamline and automate patient communication for a healthcare clinic. This is a public showcase version of a private production project — with sensitive data and secrets removed — to demonstrate architecture, code style, and bot workflow.

---

## ✨ Features

- 📲 **Telegram Bot** built with `TeleBot` (PyTelegramBotAPI)
- 🏥 **Patient Registration** flow with validation (name, phone, email, birthdate)
- 👨‍⚕️ **Doctor Selection** based on city
- 🧪 **Analysis & Appointment Booking** workflows
- 🛠️ **Technical Support + Admin escalation** logic
- 💬 **Ask custom questions** with dynamic routing
- 📝 **Binotel CRM Integration** (mocked here for security)
- ✅ **Fully Dockerized** with separate environments for dev and test
- 🔍 Clean code with full `flake8`, `pytest`, and Django structure

---

## 🛠️ Stack

- Python 3.10
- Django 5.x
- TeleBot (PyTelegramBotAPI)
- PostgreSQL
- Docker + Docker Compose
- Binotel API (credentials removed)
- Flake8 / Isort / Pytest

---

## 🚀 Local Setup

> Clone this repo and run with Docker:

```bash
git clone https://github.com/lovkiisanya/productbot-showcase.git
cd productbot-showcase
docker-compose up --build

⚠️ The .env, secret keys, and Binotel credentials are stripped out for security. Replace them with dummy/test values if you wish to explore locally.

🤖 Bot Flow Example

User → /start
↳ Selects city (e.g., Kyiv)
↳ Chooses analysis or doctor
↳ Registers or shares number
↳ Receives admin support or CRM follow-up

📁 Project Structure
User → /start
↳ Selects city (e.g., Kyiv)
↳ Chooses analysis or doctor
↳ Registers or shares number
↳ Receives admin support or CRM follow-up

🧠 Why This Project?
This bot automates patient onboarding and communication for a real-world clinic. The private version powers registration, CRM syncing, and admin alerts. This public version demonstrates my ability to:

Design scalable bot logic

Integrate APIs and databases

Structure Django/Telegram code cleanly

Write maintainable, production-ready Python

🙌 Author
Sanya Lovkii
Telegram: @lovkiisanya
GitHub: github.com/lovkiisanya

🧼 Disclaimer
This is a showcase version. No real patient data or secrets are included. Binotel and Telegram tokens are removed. """

Write the README.md file
readme_path = Path("README.md") readme_path.write_text(readme_content, encoding="utf-8")
