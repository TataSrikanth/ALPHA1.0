# 🤖✨ SkinCare Chatbot using Flask | NLP + MySQL + Admin Dashboard ✨🩺

Welcome to the official repository of **SkinCare Chatbot**! 🚀 This project is an intelligent AI-powered chatbot designed to answer skincare-related queries using Natural Language Processing (NLP). Built with **Flask**, **MySQL**, **Sentence Transformers**, and a beautiful Admin Dashboard.

## 🎥 Watch the Demo

[![SkinCare Chatbot Demo](https://img.youtube.com/vi/4MwdvFRCUos/0.jpg)](https://www.youtube.com/watch?v=4MwdvFRCUos)

---

## 🗂️ Features

- 💬 Smart Chatbot for skincare questions using semantic search
- 👤 User Registration & Login
- 🕘 Chat History with timestamp tracking
- 🧑‍💼 Admin Panel with:
  - User Management (Edit / Block / Unblock / Delete)
  - View Individual User Chat History
  - Export All Chats to CSV
  - Add / Delete Q&A Entries
  - Live User & Chat Analytics (Top Users + Daily Chats)
- 🧠 Semantic Matching via Sentence Transformers
- 🧽 Preprocessing using spaCy, NLTK, WordNet
- 🌐 Clean Bootstrap 5 UI with optional Dark Mode

---

## 🏗️ Tech Stack

| Tool / Library           | Purpose                            |
|--------------------------|------------------------------------|
| **Python + Flask**       | Backend Framework 🐍              |
| **MySQL + SQLAlchemy**   | Database 💾                       |
| **Bootstrap 5**          | Frontend Styling 🎨               |
| **Sentence Transformers**| NLP Embeddings 🔥                |
| **NLTK + spaCy**         | Text Cleaning & Synonyms 🗣️      |

---

## 📁 Directory Structure

```bash
├── app.py                # Main Flask application
├── skin_problems_QA.csv  # Dataset of Skin Problems Q&A
├── templates/            # HTML Templates
├── static/               # CSS, JS, Images
└── README.md             # This file
```

---

## 🚀 Installation & Usage

1️⃣ **Clone the repository:**
```bash
git clone https://github.com/JiteshShelke/skin-care-chatbot.git
cd skin-care-chatbot
```

2️⃣ **Install dependencies:**
```bash
pip install -r requirements.txt
```

3️⃣ **Setup MySQL Database:**
- Create a database: `chatbot_db`
- Import provided SQL tables or create manually:
  - `users`
  - `admins`
  - `chat_history`

4️⃣ **Run the application:**
```bash
python app.py
```

5️⃣ **Open Browser:**
```
http://127.0.0.1:5000
```

---

## 🔑 Default Admin Login
```
Username: admin
Password: admin123
```

(You can change it in the MySQL `admins` table)

---


## 📊 Analytics Included
- Daily Chat Volume 📅
- Top 5 Active Users 👑
- Export Chat Logs 📁

---

## 🛠️ Future Enhancements
- ✅ Responsive Mobile UI
- ✅ Token-based API for chatbot integration
- ✅ Google Login / OAuth2
- ✅ Suggestions/Correction for user queries

---

## 🤝 Contributing
Pull requests are welcome! Feel free to fork, modify, and contribute.

---

## 🔗 Connect with Me

- 🌐 [LinkedIn](https://www.linkedin.com/in/jitesh-shelke-702745286/)
- 💻 [GitHub](https://github.com/JiteshShelke)

⭐ **If you liked this project, don't forget to star the repo!** ⭐

---

## 📜 License
MIT License © 2025 Jitesh Shelke
