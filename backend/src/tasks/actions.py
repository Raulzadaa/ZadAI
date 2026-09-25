def create_file(path_dir: str, file_name: str, content: str, obsidian: bool = False) -> str:

    print("-"*40)
    print(f"path: {path_dir}, name: {file_name}")
    print("-"*40)

    if obsidian:
        # path_dir = OBSIDIAN_PATH
        path_dir = ("/home/raulzada/Obsidian/Zada/")

    with open(f"{path_dir}{file_name}", "a", encoding="UTF-8") as file:
        file.write(content) 

    return "File generated with success!"

def next_function():
    pass

# crie um arquivo app.py no caminho /home/raulzada/Projects/ZadAI/ usando FastAPI com 3 routas, 1 para autenticacao, outra para expor o projeto algo como a documentacao e ambicoes, 1 para realizar a autenticacao, 1 para usar uma IA que tenho rodando localmente, no caso Zadai