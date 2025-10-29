# 📚 Intelligent PDF Chatbot with Contextual Memory and Graph Integration

A full-stack AI-powered chatbot that answers questions based on uploaded PDFs. It uses FastAPI for backend, Streamlit for frontend, LangChain + Ollama for LLMs, MongoDB for chunk storage, Neo4j for graph linking, and Langfuse for observability.

---

## 🚀 Features

- 🔐 User registration and login (JWT-based)
- 📁 Upload up to 2 PDFs per project
- 🧠 Chunking and embedding of PDF content
- 🕸️ Graph linking via Neo4j
- 💬 Chatbot answers based on selected project
- 🧵 Session memory for chat history
- 🗑️ Delete projects and PDFs
- 📊 Langfuse integration for tracing and debugging

---

## 🧱 Tech Stack

| Layer        | Tools Used                     |
|--------------|--------------------------------|
| Backend      | FastAPI, MongoDB, Neo4j        |
| Embeddings   | LangChain + Ollama             |
| Frontend     | Streamlit                      |
| Auth         | JWT                            |
| Observability| Langfuse                       |

---

## 📁 Project Structure

RagWATI/ ├── Backend/ │
├── main.py # FastAPI entry point │
├── auth.py # User login/register │ 
├── db_mongo.py # MongoDB connection │ 
├── db_neo4j.py # Neo4j connection │
├── services_pdf.py # PDF processing & embedding │
├── services_query.py # Chunk retrieval & chatbot │ 
└── utils.py # JWT, hashing, etc. │
├── frontend/ │ 
├── app.py # Streamlit UI │
├── auth.py # Frontend auth logic │
├── utils.py # PDF upload, chat, delete
│ └── background.css # UI background styling │ 
├── .env # Environment variables 
└── README.md # Project documentation

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/RagWATI.git
cd RagWATI
###2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
###3.install dependencies
pip install -r requirements.txt
###4. set up .env
MONGO_URI=mongodb://localhost:27017
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

LANGFUSE_PUBLIC_KEY=pk-lf-9e20531d-4b32-4064-a179-11617c89e78e
LANGFUSE_SECRET_KEY=sk-lf-2aa4780d-4c80-4041-8a96-d3f3ce20a1c5
LANGFUSE_HOST=https://us.cloud.langfuse.com
###5. start backend
uvicorn Backend.main:app --reload --port 8080
###6.start front end
streamlit run frontend/app.py
###7.🧪 Testing Langfuse Integration
Visit Langfuse Dashboard

Check traces for each LLM call

View inputs, outputs, latency, retries, and prompt versions
