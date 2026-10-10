import ollama
import json

from backend.config.config import IA_CONTENT, ROUTER_SCHEMA
from backend.src.tasks.actions import create_file
from backend.src.tasks.manager import tools

def extract_json(text: str) -> dict:
    decoder = json.JSONDecoder()
    text = text.strip()
    # remove blocos de código markdown, se vierem
    if text.startswith("```"):
        text = text.strip("`").lstrip("json").strip()
    obj, idx = decoder.raw_decode(text)
    return obj

class LLMModule:
    def __init__(self):

        self.models = {
            "model_general" : "qwen3.5:9b",
            "model_coder" : "qwen2.5-coder",
            "model_search" : "qwen3.5:9b"
        }
    
        self.model_orchestrator = "qwen3.5:0.8b"
        

    def prompt(self, prompt):
        print("Thinking ...")
        response = ollama.chat(
            model=self.model_orchestrator,
            messages=[
                {"role": "system", "content": IA_CONTENT},
                {"role": "user", "content": prompt}
            ],
            think=False,
            format=ROUTER_SCHEMA
        )

        try:
            nosj = extract_json(response["message"]["content"])
        except ValueError:
            # JSON quebrado: segue para o modelo geral com o pedido original
            return self.task_prompt("general", prompt)

        category = nosj["category"].strip().lower()
        answer = (nosj.get("answer") or "").strip()
        print(nosj)

        if category == "direct" and answer:
            return answer

        if category not in ("general", "coder", "search"):
            category = "general"

        return self.task_prompt(category, nosj["prompt"])


    def task_prompt(self,model,prompt):
        model_key = f"model_{model}"
        model_name = self.models.get(model_key, self.models["model_general"])

        extra = ", for standard use python 3.13 or newest" if model == "coder" else ""
        system_msg = (
            f"Ur name is ZadAI, never use emote, only response in utf-8{extra}. "
            "When the task result is meant to be a file, you MUST call the create_file function "
            "to write it — do not just output the content as plain text."
        )


        response = ollama.chat(
            model = self.models[f"model_{model}"],
            messages=[
                {
                    "role":"system",
                    "content": system_msg
                },
                {
                    "role":"user",
                    "content": prompt
                }
            ],
            tools=tools,
            think=False
        )

        if response.get("message", {}).get("tool_calls"):
            tool_calls = response["message"]["tool_calls"]

            for tool in tool_calls:
                if tool["function"]["name"] == "create_file":
                    args = tool["function"]["arguments"]
                    print(f"\n[AI solicited call funtions] args: {args}")

                    result = create_file(
                        path_dir=args.get("path_dir",""),
                        file_name=args.get("file_name"),
                        content=args.get("content"),
                        obsidian=args.get("obsidian",True)
                    )

            return result

        else:
            return response["message"]["content"]