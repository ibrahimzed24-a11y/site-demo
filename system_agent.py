import subprocess
import os
import json
import re
import ollama

SYSTEM_PROMPT = """You are an autonomous macOS System & Coding Agent.
Execute terminal commands and manage files in the project workspace.

Respond ONLY with a valid raw JSON object. Do not wrap in markdown or add explanations.

Schema:
{
  "actions": [
    {"type": "command", "cmd": "shell command here"},
    {"type": "write_file", "path": "relative/path/to/file", "content": "file content"}
  ],
  "summary": "Short summary of actions taken"
}
"""

class SystemAgent:
    def __init__(self, model: str = "qwen2.5:7b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.client = ollama.Client(host=base_url)

    def execute_command(self, cmd: str) -> str:
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=120
            )
            out = result.stdout if result.returncode == 0 else (result.stderr or result.stdout)
            return out.strip()
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def write_file(self, path: str, content: str) -> str:
        try:
            parent_dir = os.path.dirname(os.path.abspath(path))
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    def extract_json(self, text: str) -> dict:
        text = text.strip()
        # Remove markdown wraps if present
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to locate the outermost {...} block
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            raise ValueError(f"Could not parse valid JSON from LLM response:\n{text}")

    def run(self, task: str) -> dict:
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": task}
                ],
                options={"temperature": 0.1}
            )

            raw_content = response["message"]["content"]
            plan = self.extract_json(raw_content)

            logs = []
            for action in plan.get("actions", []):
                act_type = action.get("type")
                if act_type == "command":
                    cmd = action.get("cmd")
                    logs.append(f"[CMD] {cmd}")
                    out = self.execute_command(cmd)
                    logs.append(f"[OUT] {out[:300]}")
                elif act_type == "write_file":
                    p = action.get("path")
                    logs.append(f"[WRITE] {p}")
                    out = self.write_file(p, action.get("content", ""))
                    logs.append(f"[OUT] {out}")

            return {
                "status": "success",
                "summary": plan.get("summary", "Task completed"),
                "logs": logs
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }