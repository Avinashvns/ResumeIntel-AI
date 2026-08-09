from fastapi import FastAPI

app = FastAPI(
    title="ResumeIntel AI",
    description="MCP-Enabled Agentic RAG Resume Intelligence System",
    version="0.1.0",
)

@app.get('/health')
def helth_check():
    return {
        "status": "healthy",
        "service": "resumeintel-ai",
        "version": "0.1.0",
    }