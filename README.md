# Enterprise RAG Platform

A full-stack AI-powered Retrieval-Augmented Generation (RAG) platform that allows authenticated users to upload documents, perform semantic search, and receive grounded answers with citations.

---

## Features

### AI / RAG Features

* Document upload (PDF, DOCX, TXT)
* Text extraction
* Intelligent chunking
* Embedding generation using Gemini
* Chroma Vector Database integration
* Semantic similarity search
* Hybrid retrieval (Vector Search + Keyword Search)
* Conversation-aware question rewriting
* Citation-aware answer generation

### Authentication & Security

* User Registration
* User Login
* JWT Authentication
* Protected backend APIs
* Token-based frontend access
* Logout functionality

### Multi-user Workspace

* User-specific document isolation
* Each user sees only their own uploaded documents
* Each user queries only their own documents
* Secure document deletion per user

### Frontend

* Professional SaaS-style UI
* Dark theme
* Document management dashboard
* Source filtering dropdown
* Answer cards with citations
* Login/Register page

### DevOps

* Dockerized backend
* Ready for deployment
* GitHub-ready structure

---

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn

### AI / LLM

* Google Gemini API
* Gemini Embeddings
* Gemini LLM

### Vector Database

* ChromaDB

### Frontend

* React
* Vite
* Axios
* CSS

### Authentication

* JWT
* Passlib

### Deployment Ready

* Docker

---

## Project Structure

```bash
enterprise-rag-platform/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── ingest.py
│   │   │   ├── query.py
│   │   │   ├── admin.py
│   │   │   └── health.py
│   │
│   ├── core/
│   ├── prompts/
│   ├── schemas/
│   ├── services/
│   └── db/
│
├── chroma_storage/
├── data/uploads/
│
├── rag-frontend/
│   ├── src/
│   └── public/
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Installation

### Backend Setup

```bash
git clone <repo-url>
cd enterprise-rag-platform

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Create `.env`

```env
GOOGLE_API_KEY=your_api_key
```

Run backend:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

Swagger:

```text
http://127.0.0.1:8001/docs
```

---

### Frontend Setup

```bash
cd rag-frontend
npm install
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5173
```

---

## Authentication Flow

1. Register user
2. Login user
3. JWT token generated
4. Token stored in localStorage
5. Token sent automatically in API requests

---

## RAG Flow

1. Upload document
2. Extract text
3. Split into chunks
4. Generate embeddings
5. Store in ChromaDB
6. Query user question
7. Retrieve relevant chunks
8. Rewrite question using conversation history
9. Generate answer using Gemini
10. Return answer with citations

---

## Login Page

![Login Page](assets/login-page.png)

## Dashboard

![Dashboard](assets/dashboard.png)

## Citation Answer

![Citation Answer](assets/citation-answer.png)

## Future Enhancements

* Cloud deployment
* Role-based access
* Team workspace
* Analytics dashboard
* Export answer as PDF
* Voice query support

---

## Author

Barath
Senior Developer / LLM Engineer
