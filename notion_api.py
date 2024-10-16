# Importa a biblioteca do Notion Client
from notion_client import Client

# Define a chave de autenticação do Notion
chave = "CHAVE-NOTION"

# Cria uma instância do Notion Client com a chave de autenticação
notion = Client(auth=chave)

# Define o ID da página pai onde a nova página será criada
page_id = "ID_PAGINA"

# Formata o ID da página pai para o formato correto
formatted_page_id = f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:]}"

# Define a função para criar uma nova página no Notion
def create_block(title, body):
    # Cria uma nova página no Notion com o título especificado
    new_page = notion.pages.create(
        # Define a página pai onde a nova página será criada
        parent={"page_id": formatted_page_id},
        # Define as propriedades da página, incluindo o título
        properties={
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": title
                    }
                }
            ]
        },
        # Inicializa a página sem blocos filhos
        children=[]
    )
    
    # Obtém o ID da página recém-criada
    page_id_new = new_page["id"]
    
    # Divide o conteúdo em partes de até 2000 caracteres
    max_length = 2000
    parts = [body[i:i + max_length] for i in range(0, len(body), max_length)]
    
    # Adiciona cada parte do conteúdo como um bloco de parágrafo à página
    for part in parts:
        notion.blocks.children.append(
            # Define o ID da página onde o bloco será adicionado
            block_id=page_id_new,
            # Define o bloco a ser adicionado
            children=[
                {
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": part
                                }
                            }
                        ]
                    }
                }
            ]
        )
    
    # Imprime uma mensagem de sucesso com os detalhes da página recém-criada
    print("Página criada com sucesso:", new_page)