import asyncio
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from browser_use import Agent
import ollama
from system_agent import SystemAgent

app = FastAPI(title="Browsing & System AI OS Service")

class OllamaChatModel:
    def __init__(self, model: str = "qwen2.5:7b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.model_name = model
        self.provider = "ollama"
        self.client = ollama.AsyncClient(host=base_url)

    async def ainvoke(self, messages, **kwargs):
        formatted_messages = []
        for msg in messages:
            role = "user"
            if hasattr(msg, "type"):
                if msg.type == "human":
                    role = "user"
                elif msg.type == "ai":
                    role = "assistant"
                elif msg.type == "system":
                    role = "system"
            content = getattr(msg, "content", str(msg))
            formatted_messages.append({"role": role, "content": content})

        response = await self.client.chat(model=self.model, messages=formatted_messages)
        
        class ResponseWrapper:
            def __init__(self, text):
                self.content = text
        return ResponseWrapper(response["message"]["content"])

class TaskRequest(BaseModel):
    task: str

async def run_browser_task(task: str):
    llm = OllamaChatModel(model="qwen2.5:7b")
    agent = Agent(task=task, llm=llm)
    await agent.run()

@app.get("/")
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "OS Agent Backend is running"}

# 1. مسار أتمتة المتصفح
@app.post("/run")
async def run_task_endpoint(req: TaskRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_browser_task, req.task)
    return {"status": "started", "type": "browser", "task": req.task}

# 2. مسار أتمتة النظام والملفات والـ Terminal
@app.post("/system-run")
async def run_system_task_endpoint(req: TaskRequest):
    try:
        sys_agent = SystemAgent()
        result = await asyncio.to_thread(sys_agent.run, req.task)
        return result
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)