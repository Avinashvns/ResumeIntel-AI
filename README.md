# ResumeIntel AI

### MCP-Enabled Agentic RAG Resume Intelligence System

ResumeIntel AI is a full-stack GenAI application that analyzes a candidate's resume against a given job description using **Retrieval-Augmented Generation (RAG)**, a **LangGraph-based Agent**, and **MCP-based tool integration**.

The system retrieves relevant information from the candidate's resume, analyzes job requirements, identifies skill gaps, and generates actionable recommendations.

---

## 🎯 Problem

Recruiters and candidates often need to manually compare resumes with job descriptions.

Traditional keyword-based matching can miss:

* Semantic similarity between skills
* Relevant project experience
* Transferable experience
* Missing or weak skills
* Context behind a candidate's experience

ResumeIntel AI aims to provide a more intelligent, context-aware analysis using modern GenAI techniques.

---

## 💡 Solution

The system follows an Agentic RAG architecture:

```text
                    User
                      │
                      ▼
                 Next.js UI
                      │
                      ▼
                 FastAPI API
                      │
                      ▼
              LangGraph Agent
                 │         │
                 ▼         ▼
              RAG Tool   MCP Tools
                 │         │
                 ▼         ▼
               FAISS   MCP Server
                 │         │
                 └────┬────┘
                      ▼
                  LLM Layer
                      │
                      ▼
               Job Analysis
                      │
                      ▼
                Final Result
```

---

## 🚀 Core Features

### Resume Intelligence

* PDF resume upload
* Text extraction
* Document cleaning
* Intelligent chunking
* Metadata extraction

### RAG Pipeline

* Hugging Face embeddings
* FAISS vector database
* Semantic search
* Top-K retrieval
* Context-aware generation
* Grounded responses

### Agentic AI

* LangGraph-based agent
* Query analysis
* Retrieval decisions
* Context quality evaluation
* Query rewriting
* Multi-step reasoning workflow

### MCP Integration

The agent will interact with MCP tools such as:

* `search_resume()`
* `get_job_requirements()`
* `save_analysis()`

MCP provides a standardized interface between the agent and external tools.

### Job Intelligence

The system will generate:

* Overall match score
* Matched skills
* Missing skills
* Relevant experience
* Job requirement analysis
* Resume improvement recommendations

### Full-Stack Application

* Next.js frontend
* FastAPI backend
* REST API
* Responsive UI
* Production deployment

---

## 🏗️ Technology Stack

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

### Backend

* Python
* FastAPI
* Pydantic

### GenAI

* LangChain
* LangGraph
* Ollama
* Qwen3

### RAG

* Hugging Face Sentence Transformers
* FAISS
* PyMuPDF

### Agent Tooling

* MCP

### Development

* Git
* Pytest
* Conda

---

## 📂 Project Structure

```text
ResumeIntel-AI/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── config/
│   │   ├── ingestion/
│   │   ├── retrieval/
│   │   ├── rag/
│   │   ├── agent/
│   │   ├── mcp/
│   │   └── llm/
│   │
│   ├── tests/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│
├── data/
│   ├── resumes/
│   └── jobs/
│
├── docs/
│
├── .gitignore
└── README.md
```

---

## 🔄 RAG Pipeline

The planned RAG pipeline is:

```text
Resume PDF
    ↓
PDF Text Extraction
    ↓
Text Cleaning
    ↓
Document Chunking
    ↓
Hugging Face Embeddings
    ↓
FAISS Vector Store
    ↓
Semantic Retrieval
    ↓
Relevant Resume Context
    ↓
LLM
    ↓
Grounded Response
```

---

## 🤖 Agent Workflow

The LangGraph agent will orchestrate the reasoning workflow:

```text
START
  ↓
Analyze Query
  ↓
Retrieve Relevant Context
  ↓
Evaluate Context
  ↓
 ┌───────────────┐
 │ Relevant?     │
 └──────┬────────┘
        │
    ┌───┴───┐
    │       │
   YES      NO
    │       │
    ▼       ▼
 Generate  Rewrite Query
    │       │
    │       ▼
    │     Retrieve
    │       │
    └───┬───┘
        ▼
       END
```

---

## 🔌 MCP Architecture

The system will use MCP for standardized tool integration.

Planned tools:

```text
MCP Server
│
├── search_resume()
│
├── get_job_requirements()
│
└── save_analysis()
```

The LangGraph agent will decide when these tools are required during the workflow.

---

## 💻 Local Development

### Requirements

* Python 3.12+
* Node.js
* Conda
* Git
* Ollama
* NVIDIA GPU recommended for local LLM inference

The project is designed to run on consumer hardware and will initially use a lightweight local LLM such as **Qwen3 4B** through Ollama.

---

## ⚙️ Backend Setup

```bash
cd backend

conda create -n resumeintel python=3.12 -y

conda activate resumeintel

pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
GET /health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "resumeintel-ai",
  "version": "0.1.0"
}
```

---

## 🖥️ Frontend Setup

Frontend development will use Next.js.

```bash
cd frontend

npm install

npm run dev
```

The frontend will communicate with the FastAPI backend through REST APIs.

---

## 🧪 Testing

The project will include tests for:

* Document ingestion
* Chunking
* Embeddings
* Vector retrieval
* RAG pipeline
* Agent workflow
* MCP tools
* API endpoints

Testing framework:

```text
Pytest
```

---

## 🌐 Deployment

The final application will be deployed as a production web application.

Planned architecture:

```text
                Internet
                   │
                   ▼
              Next.js App
                   │
                   ▼
              FastAPI API
                   │
                   ▼
            LangGraph Agent
              │         │
              ▼         ▼
             RAG       MCP
              │         │
              ▼         ▼
            FAISS   MCP Server
              │         │
              └────┬────┘
                   ▼
                  LLM
```

The development environment will use **Ollama + Qwen3** for local inference. Production LLM inference may use a hosted model/API depending on deployment requirements and cost.

---

## 📈 Project Status

### Phase 1 — Foundation

* [x] Project initialization
* [x] Backend structure
* [x] FastAPI foundation
* [x] Health endpoint

### Phase 2 — Resume Ingestion

* [ ] PDF upload
* [ ] Text extraction
* [ ] Text cleaning
* [ ] Chunking
* [ ] Metadata

### Phase 3 — RAG

* [ ] Embeddings
* [ ] FAISS
* [ ] Retriever
* [ ] LangChain RAG
* [ ] Grounded generation

### Phase 4 — Agent

* [ ] LangGraph state
* [ ] Query analysis
* [ ] Retrieval node
* [ ] Context evaluation
* [ ] Query rewriting
* [ ] Final generation

### Phase 5 — MCP

* [ ] MCP server
* [ ] Resume search tool
* [ ] Job requirement tool
* [ ] Analysis persistence tool
* [ ] Agent + MCP integration

### Phase 6 — Job Intelligence

* [ ] Job description parsing
* [ ] Skill matching
* [ ] Missing skill detection
* [ ] Experience matching
* [ ] Match score
* [ ] Recommendations

### Phase 7 — Full Stack

* [ ] Next.js UI
* [ ] Resume upload
* [ ] Job description input
* [ ] Analysis dashboard
* [ ] Agent activity
* [ ] Error/loading states
* [ ] Responsive UI

### Phase 8 — Production

* [ ] Automated tests
* [ ] Input validation
* [ ] Production error handling
* [ ] Logging
* [ ] Production configuration
* [ ] Backend deployment
* [ ] Frontend deployment
* [ ] Live demo

---

## 🎯 Learning & Engineering Goals

This project is designed to demonstrate practical knowledge of:

```text
RAG
↓
Embeddings
↓
Vector Databases
↓
Semantic Retrieval
↓
LangChain
↓
LangGraph
↓
Agentic Workflows
↓
MCP
↓
Tool Calling
↓
LLM Integration
↓
FastAPI
↓
Next.js
↓
Testing
↓
Deployment
```

---

## 🔮 Future Improvements

Possible future extensions:

* Advanced reranking
* Hybrid search
* Better evaluation metrics
* Authentication
* Persistent database
* Resume version comparison
* Multiple job comparison
* Observability
* Feedback-based retrieval improvement

These features are intentionally outside the initial project scope.

---

## 👨‍💻 Author

**Avinash Singh**

Built as a practical GenAI / LLM Engineering project focused on **RAG, Agentic AI, MCP, and production deployment**.

---

## 📄 License

This project is intended for educational and portfolio purposes.
