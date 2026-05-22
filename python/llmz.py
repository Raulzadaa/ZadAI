import ollama

class Llmz:
    def __init__(self):

        self.model = "qwen2.5:7b"
        self.phrase = []

    def prompt(self, prompt):
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role":"system",
                    "content": "u is a virutal assistent called ZadAI, and if dont request a long response, u just send a resumed response"
                },
                {
                    "role":"user",
                    "content": prompt
                }
            ],

        )

        return response["message"]["content"]