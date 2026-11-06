import asyncio
from browser_use import Agent
import ollama

class OllamaChatModel:
    def __init__(self, model: str = "qwen2.5:7b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.model_name = model  # الخاصية المطلوبة لإصلاح الـ AttributeError
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

async def main():
    llm = OllamaChatModel(model="qwen2.5:7b")
    agent = Agent(
        task="Go to google.com and search for 'Browsing AI OS' and print the title of the first result",
        llm=llm,
    )
    result = await agent.run()
    print("\n--- Execution Result ---\n")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())