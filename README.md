# 🤖 AI-Powered GitHub Repository Summarizer

An intelligent backend service that analyzes any public GitHub repository and generates a concise summary, technology stack, and project structure using a **cost-efficient LangGraph pipeline** and Large Language Models.

Built with **FastAPI + LangChain + LangGraph + NVIDIA/Azure LLMs**, this system demonstrates production-grade Agentic AI architecture.

---

## 🌟 Key Features

✅ Analyze any public GitHub repository  
✅ Metadata-first retrieval (token-efficient)  
✅ Deterministic quality gate (no unnecessary LLM calls)  
✅ Intelligent fallback deep-dive for sparse repos  
✅ Structured LLM output with Pydantic validation  
✅ Provider-agnostic LLM factory (NVIDIA / Azure OpenAI)  
✅ Production-ready FastAPI backend  
✅ Centralized exception handling & logging  
✅ Secure GitHub API integration with token auth  

---

## 🧠 How It Works (Architecture)

Instead of downloading entire repositories, the system uses a **Selective Context Retrieval pipeline**:

```

GitHub URL
↓
Inspector → Fetch repo tree & detect key files
↓
Scorer → Heuristic quality evaluation
↓
Collector (if sufficient signals)
OR
Deep Dive (if insufficient signals)
↓
Context Builder → Structured payload
↓
Summarizer → LLM synthesis
↓
Structured Output

```

### 🎯 Why This Design?

✔ Reduces token usage  
✔ Minimizes latency  
✔ Improves accuracy  
✔ Handles large repositories safely  
✔ Avoids LLM hallucination  

---

## 🏗️ LangGraph Workflow

The pipeline is implemented as a **stateful graph**:

```

Inspector → Scorer → Collector / Deep Dive → Context Builder → Summarize

`````

### 🔍 Node Responsibilities

| Node | Purpose |
|------|---------|
Inspector | Fetch repo metadata via GitHub API |
Scorer | Determine if context is sufficient |
Collector | Download high-signal files |
Deep Dive | Fallback exploration |
Context Builder | Prepare structured context |
Summarizer | Generate final analysis |

---

## 🧪 Example API Usage

### 📥 Request

````http
POST /summarize
Content-Type: application/json
`````

```json
{
  "github_url": "https://github.com/psf/requests"
}
```

---

### 📤 Response

```json
{
  "summary": "A popular Python HTTP client library...",
  "technologies": ["Python", "HTTP"],
  "structure": "Library-style project with modules and tests"
}
```

---

## ⚙️ Tech Stack

### 🧩 Backend

* FastAPI
* Python 3.10+
* Async architecture

### 🤖 AI & LLM

* LangChain
* LangGraph
* NVIDIA AI Endpoints (Llama-3)
* Azure OpenAI (optional)

### 🔗 External APIs

* GitHub REST API

### 🧠 Architecture Patterns

* Service layer pattern
* Factory pattern (LLM provider)
* DTO pattern
* Centralized exception handling

---

## 📁 Project Structure

```

app/
├── api/                # FastAPI controllers
├── core/               # Config & logger
├── dto/                # Request/response schemas
├── exceptions/         # Custom exceptions & handlers
├── graph/              # LangGraph workflow
│   └── nodes/          # Individual graph nodes
├── llm/                # Model factory
├── providers/          # GitHub API integration
├── service/            # Business logic layer
├── utils/              # HTTP utilities
└── main.py             # Application entry point

```

---

## 🔐 Environment Configuration

Create a `.env` file:

```env
LLM_PROVIDER=nvidia

NVIDIA_API_KEY=your_nvidia_api_key
NVIDIA_MODEL=meta/llama-3.1-70b-instruct
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1

GITHUB_TOKEN=your_github_token

LLM_TEMPERATURE=0.2

AZURE_API_KEY=Enter_Your_AZURE_API_KEY
AZURE_ENDPOINT=Enter_Your_AZURE_ENDPOINT
AZURE_MODEL=Enter_Your_AZURE_MODEL
AZURE_API_VERSION=Enter_Your_AZURE_API_VERSION
AZURE_DEPLOYMENT_NAME=enter_AZURE_DEPLOYMENT_NAME


```

---

## 🚀 Running Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/GovindaTak/repo-summarizer-github-agent.git
cd repo-summarizer-github-agent
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Start Server

```bash
uvicorn app.main:app --reload
```

---

### 5️⃣ Open Swagger UI

👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧩 Design Highlights

### 💎 Token-Efficient Retrieval

The system never sends full repositories to the LLM.

### 🧮 Deterministic Quality Gate

A rule-based scoring system ensures predictable behavior.

### 🧠 Structured Output

LLM responses are validated using Pydantic models.

### 🔄 Provider-Agnostic LLM Factory

Easily switch between NVIDIA and Azure OpenAI.

---

## ⚠️ Limitations

* Currently supports public repositories only
* Large monorepos may require deeper traversal logic
* Private repo access requires appropriate token permissions

---

## 🛣️ Future Improvements

* Caching repository metadata
* Support for private repositories
* Parallel file retrieval
* Streaming responses
* UI dashboard
* Multi-repo comparison

---

## 👨‍💻 Author

**Govinda Tak**

AI Engineer | Backend Developer | GenAI Enthusiast

---
