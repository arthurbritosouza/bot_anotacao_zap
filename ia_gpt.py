import base64
import openai
import os



openai.api_key = "sk-lU_zIGpHnl2LspJtaHoUbbrpE1Hf6dQBH6GSaS8Nq8T3BlbkFJuvGVVqQHog1IPCnpHR5IrkiuaiEP6aJCOk0-4welMA"

def codificar_imagem_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as imagem:
        imagem_base64 = base64.b64encode(imagem.read()).decode('utf-8')
        print(imagem_base64)
    return imagem_base64
caminho_da_imagem = "_foto/image.jpeg"


def analisar_image(caminho_da_imagem):
    imagem_base64 = codificar_imagem_base64(caminho_da_imagem)
    
    prompt = f"oi chat tudo bem?"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        temperature=0,
        menssages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message['content']


if __name__ == "__main__":
    analisar_image(caminho_da_imagem)


