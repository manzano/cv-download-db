import requests
import sys
from tqdm import tqdm
import os
import itertools
import threading
import time
import subprocess
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Função para limpar a tela do terminal
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Carrega as variáveis de ambiente
email = os.getenv('EMAIL')
token = os.getenv('TOKEN')
subdomain = os.getenv('SUBDOMAIN')

# URL da API
url_api = f'https://{subdomain}.cvcrm.com.br/api/v2/cv/downloadDB'
headers = {
    'email': email,
    'token': token
}

# Diretório onde o arquivo será salvo
diretorio_dados = './dados/'  # Caminho relativo

# Variável global para controlar o fim do "loading"
done_loading = False

# Função para limpar a pasta dados antes do download
def limpar_pasta_dados():
    if os.path.exists(diretorio_dados):
        for arquivo in os.listdir(diretorio_dados):
            caminho_arquivo = os.path.join(diretorio_dados, arquivo)
            try:
                if os.path.isfile(caminho_arquivo):
                    os.unlink(caminho_arquivo)
                    print(f"Arquivo {arquivo} removido da pasta dados.")
            except Exception as e:
                print(f"Erro ao remover o arquivo {arquivo}: {e}")
    else:
        os.makedirs(diretorio_dados)  # Cria a pasta se não existir
        print(f"Pasta {diretorio_dados} criada.")

# Função para simular um "loading" em segundo plano
def loading_animation():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done_loading:
            break
        sys.stdout.write('\rFazendo requisição para a API... ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rRequisição completa!        \n')

# Função para fazer a requisição à API
def fazer_requisicao():
    global done_loading
    limpar_tela()  # Limpa a tela assim que o script começa a ser executado
    limpar_pasta_dados()  # Limpa a pasta dados antes do download
    
    # Inicia a thread com a animação de loading
    done_loading = False
    t = threading.Thread(target=loading_animation)
    t.start()

    try:
        response = requests.get(url_api, headers=headers)
        
        # Para a animação de loading
        done_loading = True
        t.join()

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            json_data = response.json()
            status = json_data.get('status')
            
            if status == 'success':
                print("Arquivo encontrado!")
                url_download = json_data['data']['urlDownload']
                password = json_data['data']['password']
                
                print(f"\nEndereço:\n{url_download}")
                print(f"\nSenha:\n{password}\n")
                
                # Baixa o arquivo e depois descriptografa
                caminho_completo = baixar_arquivo(url_download)
                if caminho_completo:
                    caminho_descriptografado = descriptografar_arquivo(caminho_completo, password)
                    if caminho_descriptografado:
                        descompactar_gz(caminho_descriptografado)
            else:
                print("Erro: Requisição não foi bem-sucedida.")
        else:
            print(f"Erro na requisição: {response.status_code}")
    
    except Exception as e:
        done_loading = True
        print(f"Erro: {e}")
        sys.exit(1)

# Função para baixar o arquivo com barra de progresso
def baixar_arquivo(url):
    try:
        print("Baixando arquivos...")
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            # Nome do arquivo extraído da URL
            nome_arquivo = url.split('/')[-1].split('?')[0]
            caminho_completo = os.path.join(diretorio_dados, nome_arquivo)
            
            # Verifica se a pasta de destino existe, senão cria
            if not os.path.exists(diretorio_dados):
                os.makedirs(diretorio_dados)
            
            # Tamanho total do arquivo em bytes
            total_tamanho = int(response.headers.get('content-length', 0))
            
            # Exibe o tamanho do arquivo em MB
            print(f"Tamanho: {total_tamanho / (1024 * 1024):.2f}MB\n")
            
            # Barra de progresso com tqdm
            with open(caminho_completo, 'wb') as f, tqdm(
                desc="Situação",
                total=total_tamanho,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # Filtro de chunks vazios
                        f.write(chunk)
                        bar.update(len(chunk))
            
            print(f"\nDownload concluído! Arquivo salvo em: {caminho_completo}")
            return caminho_completo
        else:
            print(f"Erro ao baixar o arquivo: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"Erro ao baixar o arquivo: {e}")
        return None

# Função para descriptografar o arquivo .gpg usando a senha fornecida
def descriptografar_arquivo(caminho_arquivo, senha):
    try:
        arquivo_descriptografado = caminho_arquivo.replace('.gpg', '')

        print("Descriptografando o arquivo...")
        
        # Comando para chamar o gpg e descriptografar o arquivo
        command = ['gpg', '--batch', '--yes', '--passphrase', senha, '-o', arquivo_descriptografado, '-d', caminho_arquivo]
        subprocess.run(command, check=True)
        
        print(f"Arquivo descriptografado com sucesso e salvo em: {arquivo_descriptografado}")
        return arquivo_descriptografado
    
    except subprocess.CalledProcessError as e:
        print(f"Erro ao descriptografar o arquivo: {e}")
        return None
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

# Função para descompactar o arquivo .gz usando o gzip pelo console e ignorar erros
def descompactar_gz(caminho_gz):
    try:
        print("Descompactando o arquivo .gz...")
        
        # Comando para rodar o gzip pelo console
        command = ['gzip', '-d', caminho_gz]
        subprocess.run(command, stderr=subprocess.DEVNULL)  # Ignorar erros
        
        arquivo_sql = caminho_gz.replace('.gz', '')
        print(f"Arquivo descompactado com sucesso e salvo em: {arquivo_sql}")
    
    except Exception as e:
        print(f"Erro ao descompactar o arquivo .gz: {e}")

# Executa a requisição
if __name__ == '__main__':
    fazer_requisicao()
