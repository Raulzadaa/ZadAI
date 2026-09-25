tools = [
    {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": (
                "Cria ou sobrescreve um arquivo local com o conteúdo fornecido. "
                "Use SEMPRE que o resultado final da tarefa for um arquivo — código-fonte "
                "(ex: .py, .js), anotações, notas do Obsidian, ou qualquer texto que o usuário "
                "pediu para salvar, escrever ou gerar como arquivo. Nunca responda apenas com "
                "o conteúdo em texto puro quando um caminho de arquivo for esperado — sempre "
                "chame esta função para efetivamente gravar o conteúdo em disco."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path_dir": {
                        "type": "string",
                        "description": "O diretório onde o arquivo será salvo. Vazio ('') apenas se obsidian for True."
                    },
                    "file_name": {
                        "type": "string",
                        "description": "O nome do arquivo com extensão (ex: 'app.py', 'diario.md')."
                    },
                    "content": {
                        "type": "string",
                        "description": "O conteúdo completo e exato a ser escrito no arquivo."
                    },
                    "obsidian": {
                        "type": "boolean",
                        "description": "True para salvar no cofre do Obsidian. Padrão: False."
                    }
                },
                "required": ["file_name", "content"],
            }
        }
    }
]