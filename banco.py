import os
import subprocess
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Carrega as variáveis de ambiente do banco de dados
db_host = os.getenv('DB_HOST')
db_usuario = os.getenv('DB_USUARIO')
db_senha = os.getenv('DB_SENHA')
db_database = os.getenv('DB_DATABASE')

# Caminho da pasta onde os arquivos .sql estão armazenados
diretorio_dados = './dados/'

# Função para importar o arquivo .sql no banco de dados
def importar_sql(arquivo_sql):
    try:
        print(f"Importando o arquivo {arquivo_sql} para o banco de dados...")

        # Comando para importar o arquivo .sql no banco de dados usando mysql
        command = [
            'mysql',
            f'-h{db_host}',
            f'-u{db_usuario}',
            f'-p{db_senha}',
            # '--verbose',
            db_database,
            '-e', f"source {arquivo_sql}"
        ]

        # Executa o comando
        subprocess.run(command, check=True)

        print(f"Arquivo {arquivo_sql} importado com sucesso no banco de dados {db_database}!")

    except subprocess.CalledProcessError as e:
        print(f"Erro ao importar o arquivo {arquivo_sql}: {e}")
    except Exception as e:
        print(f"Erro inesperado ao importar o arquivo {arquivo_sql}: {e}")

# Função principal para encontrar e importar todos os arquivos .sql na pasta dados
def importar_arquivos_sql():
    try:
        # Percorre todos os arquivos na pasta dados
        for arquivo in os.listdir(diretorio_dados):
            if arquivo.endswith('.sql'):
                caminho_completo = os.path.join(diretorio_dados, arquivo)
                importar_sql(caminho_completo)
    
    except Exception as e:
        print(f"Erro ao ler os arquivos da pasta {diretorio_dados}: {e}")

# Executa a importação
if __name__ == '__main__':
    importar_arquivos_sql()
