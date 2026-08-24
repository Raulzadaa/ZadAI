import ollama

class LLMModule:
    def __init__(self):

        self.model = "qwen3:8b"
        self.phrase = []

    def prompt(self, prompt):
        print("Thinking ...")
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role":"system",
                    "content": "u is a virutal assistent called ZadAI. ,dont use emoji or simblo and if dont request a long response, u just send a resume response"
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