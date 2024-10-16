import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

contato_autorizado = None
ultima_msg_lida = None
def verificar_contato_atual(driver):
    """
    Verifica se o contato atual tem uma mensagem com o comando /start
    e se sim, atualiza a variável global contato_autorizado
    """
    global contato_autorizado
    try:
        while True:
            # Encontra o header com o nome do contato atual
            header_xpath = '//header//span[@dir="auto"]'
            contato_atual = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, header_xpath)))
            if contato_atual:
                # Espera 3 segundos para que a página carregue as mensagens
                time.sleep(3)
                print("tem contato atual")
                # Encontra todas as mensagens enviadas pelo contato atual
                todas_mensagens = driver.find_elements(By.CLASS_NAME, 'message-out')
                # Encontra a última mensagem enviada pelo contato atual
                msg_funcao = todas_mensagens[-1].find_element(By.CLASS_NAME, 'selectable-text')
            else:
                print("não tem contato atual")

            # Verifica se a última mensagem do contato atual é o comando /start
            if msg_funcao.text == "/start" and contato_autorizado == None:
                # Atualiza a variável global contato_autorizado com o nome do contato atual
                contato_autorizado = contato_atual.text
                print(f"Contato autorizado: {contato_autorizado}\n")
                # Retorna o nome do contato atual
                return contato_autorizado

            # Verifica se o contato atual é o mesmo que o contato autorizado
            elif contato_autorizado == contato_atual.text:
                # Retorna o nome do contato atual
                return contato_autorizado
            else:
                # Imprime uma mensagem de erro se o contato atual não recebeu o comando /start
                print(f"Contato atual não recebeu o comando /start: {contato_atual.text}\n")
                
            
    except Exception as e:
        # Verifica se o erro é um "stale element reference"
        if "stale element reference" in str(e):
            # Tenta buscar a última mensagem novamente
            print("Elemento stale, recarregando...")
            return verificar_contato_atual(driver)
        else:
            # Imprime uma mensagem de erro se o erro não é um "stale element reference"
            print(f"Erro ao buscar última mensagem: {e}")
                
def ultima_mensagem(driver):
    """
    Verifica se o contato atual tem uma nova mensagem e se sim,
    atualiza a variável global ultima_msg_lida e retorna a mensagem
    """
    global contato_autorizado, ultima_msg_lida
    if contato_autorizado != None:
        try:
            # Encontra todas as mensagens enviadas pelo contato atual
            todas_mensagens = driver.find_elements(By.CLASS_NAME, 'message-out')
            if todas_mensagens:
                # Encontra a mensagem anterior
                msg_anterior = todas_mensagens[-2].find_element(By.CLASS_NAME, 'selectable-text')
                print(f"mensagem anterios: {msg_anterior.text}")
                # Encontra a última mensagem enviada pelo contato atual
                ultima_mensagem = todas_mensagens[-1].find_element(By.CLASS_NAME, 'selectable-text')
                
                # Verifica se a última mensagem do contato atual é o comando /stop
                if ultima_mensagem.text == "/stop" and contato_autorizado:
                    print("Retirando a authenticação")
                    contato_autorizado = None
                    return "Contato Parado" 
                # Verifica se a mensagem anterior é igual a mensagem atual
                elif ultima_msg_lida == ultima_mensagem.text:
                    print("Última mensagem já foi lida, ignorando...")
                    return ""
                else:
                    # Nova mensagem recebida
                    print(f"Última mensagem enviada: {ultima_mensagem.text}\n")
                    ultima_msg_lida = ultima_mensagem.text  # Atualiza a última mensagem lida
                    return ultima_mensagem.text
            else:
                print("Nenhuma mensagem enviada encontrada")
                
        except Exception as e:
            # Verifica se o erro é um "stale element reference"
            if "stale element reference" in str(e):
                # Tenta buscar a última mensagem novamente
                print("Elemento stale, recarregando...")
                return ultima_mensagem(driver)
            else:
                # Imprime uma mensagem de erro se o erro não é um "stale element reference"
                print(f"Erro ao buscar última mensagem: {e}")
    else:
        print(f"Contato não está ativo")


"""
Esta função representa o loop principal para processamento de mensagens do WhatsApp.
Ela verifica contatos autorizados e processa suas mensagens de acordo.
"""
if __name__ == '__main__':
    # Obtenha o caminho do diretório atual
    dir_path = os.getcwd()


    # Configure as opções do Chrome
    options = Options()
    options.add_argument(r"user-data-dir=" + os.path.join(dir_path, "profile/zap"))


    # Inicialize o webdriver do Chrome
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")


    # Aguarde a página do WhatsApp web carregar
    WebDriverWait(driver, 60).until(    
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]'))
    )
    
    while True:
        try:
            if contato_autorizado is None:
                print("Verificando novo contato...")
                # Verifique e atualize o contato autorizado
                contato_autorizado = verificar_contato_atual(driver)
            else:
                # Processa as novas mensagens para o contato autorizado
                print(f"Processando mensagens para contato autorizado: {contato_autorizado}")
                resultado = ultima_mensagem(driver)


        except Exception as e:
            print(f"Erro no loop principal: {e}")


        time.sleep(5)  # Evite sobrecarregar o processo
