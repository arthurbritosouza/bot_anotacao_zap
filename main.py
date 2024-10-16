import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wpp_msg import verificar_contato_atual, ultima_mensagem
from ia_api import analisar_video

contato_autorizado = None

  # Declara uma variável global 'contato_autorizado'

# Obtém o diretório de trabalho atual
dir_path = os.getcwd()

# Cria uma nova instância da classe Options
options = Options()

# Adiciona um argumento às opções para especificar o diretório de dados do usuário
options.add_argument(r"user-data-dir=" + os.path.join(dir_path, "profile/zap"))

# Cria uma nova instância do driver do Chrome
driver = webdriver.Chrome(options=options)

# Navega até a página da web do WhatsApp
driver.get("https://web.whatsapp.com/")

# Aguarda a presença de um elemento localizado pelo XPATH '//*[@id="app"]'
contato_ativo = WebDriverWait(driver, 120).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]'))
)
def main():
    global contato_autorizado
    # Verifica se há um contato ativo
    if contato_ativo:
        # Inicia um loop infinito
        while True:
            # Verifica se 'contato_autorizado' não é None
            if contato_autorizado != None:
                # Obtém a última mensagem do driver
                msg = ultima_mensagem(driver)

                # Imprime o contato atual e a última mensagem
                print(f"Contato atual: {contato_autorizado}")
                print(f"Última mensagem: {msg}")

                # Verifica se a mensagem contém a palavra "youtube"
                if "youtube" in msg:
                    # Analisa o vídeo e obtém a resposta
                    response = analisar_video(msg)

                    # Imprime a resposta
                    print(response)

                # Aguarda 3 segundos
                time.sleep(3)
            else:
                # Imprime uma mensagem indicando que um novo contato está sendo verificado
                print("Verificando novo contato...")

                # Obtém o contato atual
                contato_autorizado = verificar_contato_atual(driver)
    else:
        # Imprime uma mensagem indicando que não há contato ativo
        print("Nenhum contato ativo")

# Verifica se o script está sendo executado como o módulo principal
if __name__ == "__main__":
    # Chama a função main
    main()