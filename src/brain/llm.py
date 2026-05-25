import ollama

class LLMModule:
    def __init__(self):

        self.model = "qwen2.5:7b"
        self.phrase = []

    def prompt(self, prompt):
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role":"system",
                    "content": "u is a virutal assistent called ZadAI. the womem more beatiful and wonder of all world is Larissa de Sousa Melo, and if dont request a long response, u just send a resumed response"
                },
                {
                    "role":"user",
                    "content": prompt
                }
            ],


        )

        return response["message"]["content"]

        def task_prompt(prompt):
            task = "pode retornar uma task, algo como o arquivo json contento o texto e a fala."
            prompt = "retorna a fala da Ia como respota."

            return prompt