# 🤖 AI Code Reviewer

An AI-powered code review system that analyzes GitHub Pull Requests, detects bugs, suggests improvements, and posts automated review comments using FastAPI, Python, and GitHub App integration.

---

## 🚀 Features  

- 🔍 Automatic GitHub Pull Request analysis  
- 🤖 AI-powered code review suggestions  
- 🐞 Bug detection and code quality analysis  
- 🔐 Security vulnerability detection  
- ⚡ Performance improvement recommendations  
- 🔗 GitHub App integration   
- 📡 REST API using FastAPI  
- 🧠 Supports AI models (Groq / OpenAI)

---

## 🏗️ Tech Stack

- Python 🐍  
- FastAPI ⚡  
- SQLAlchemy 🗄️  
- PostgreSQL 🐘  
- Redis 🔴  
- GitHub App API 🔗  
- AI API (Groq/OpenAI) 🤖  
- Uvicorn 🚀  

---

## 📁 Project Structure
ai-code-reviewer-main/
│
├── app/
│ ├── api/
│ │ └── webhook.py
│ ├── services/
│ │ └── github_service.py
│ ├── db/
│ │ ├── database.py
│ │ └── models.py
│
├── main.py
├── requirements.txt
├── .env
└── private-key.pem (not included in repo)
---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Alishainamdar17/AI-Code-Reviewer-Alisha.git
cd AI-Code-Reviewer-Alisha
