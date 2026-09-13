tools = [
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Cria ou adiciona conteúdo a um arquivo local. Use sempre que o usuário pedir para anotar, salvar, criar uma nota ou escrever em um arquivo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path_dir": {
                        "type": "string",
                        "description": "O diretório onde o arquivo será salvo (pode ser vazio se obsidian for True)."
                    },
                    "file_name": {
                        "type": "string",
                        "description": "O nome do arquivo com extensão (ex: 'diario.md', 'tarefas.txt')."
                    },
                    "content": {
                        "type": "string",
                        "description": "O texto exato que deve ser escrito dentro do arquivo."
                    },
                    "obsidian": {
                        "type": "boolean",
                        "description": "Define se o arquivo deve ir para o cofre do Obsidian. Padrão é True."
                    }
                },
                "required": ["file_name", "content"], # Apenas os essenciais, já que path e obsidian têm regras/valores padrão
            }
        }
    }
]