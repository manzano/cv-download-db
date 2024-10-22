
# **Projeto CV-Download-DB**

Este projeto tem como objetivo baixar, descriptografar e descompactar um arquivo de backup do banco de dados, e, posteriormente, importar os dados para o banco MySQL.

## **Aviso Importante**

Este projeto foi desenvolvido como um recurso educacional e de orientação para os clientes. Ele não é mantido pelo CV CRM, e você está livre para copiá-lo e modificá-lo conforme necessário.

## **Pré-requisitos**

Antes de começar, você precisará ter instalado no seu sistema as seguintes ferramentas:

- **Python 3.x**
- **GnuPG** para descriptografar o arquivo `.gpg`
- **MySQL** para importar os dados.

### **Instalando o GnuPG**

#### **No macOS** (via Homebrew):
```bash
brew install gnupg
```

#### **No Linux (Ubuntu/Debian):**
```bash
sudo apt-get install gnupg
```

#### **No CentOS/Fedora:**
```bash
sudo yum install gnupg
```

#### **No Windows:**

Baixe e instale o **Gpg4win** pelo link:

[https://gpg4win.org/download.html](https://gpg4win.org/download.html)

Após instalar, adicione o GnuPG ao `PATH` do sistema para poder executá-lo no terminal.

---

## **Configuração do Projeto**

### 1. **Clonando o repositório**
Baixe ou clone o repositório do projeto no seu sistema. Se você estiver usando `git`, pode usar o seguinte comando:

```bash
git clone https://github.com/manzano/cv-download-db.git
cd cv-download-db
```

### 2. **Criando o ambiente virtual**

Para garantir que todas as dependências sejam instaladas corretamente, você precisa criar e ativar um ambiente virtual. Siga os passos abaixo:

#### **Passos para criar e ativar o ambiente virtual:**

- **Linux/macOS**:
    ```bash
    python3 -m venv venv  # Cria o ambiente virtual
    source venv/bin/activate  # Ativa o ambiente virtual
    ```

- **Windows**:
    ```bash
    python -m venv venv  # Cria o ambiente virtual
    venv\Scripts\activate  # Ativa o ambiente virtual
    ```

Após ativar o ambiente, todas as bibliotecas serão instaladas localmente dentro dele.

### 3. **Instalando as dependências**

Com o ambiente virtual ativado, agora você precisa instalar as dependências necessárias para rodar o projeto. Para isso, basta usar o comando:

```bash
python3 -m pip install -r requirements.txt
```

Este comando instalará todas as bibliotecas listadas no arquivo `requirements.txt`, como `requests`, `tqdm`, `python-dotenv` e outras dependências.

---

## **Configuração do Banco de Dados**

Antes de executar o script, configure o banco de dados MySQL em seu sistema. Crie um arquivo `.env` na raiz do projeto com as informações do banco de dados:

Você pode usar o arquivo exemplo.env como referência.

### Exemplo de arquivo `.env`:

```bash
DB_HOST=localhost
DB_USUARIO=seu_usuario
DB_SENHA=sua_senha
DB_DATABASE=nome_do_banco
EMAIL=seu_email
TOKEN=seu_token
SUBDOMAIN=seu_subdominio
```

- `DB_HOST`: Endereço do servidor MySQL (ex: localhost).
- `DB_USUARIO`: Usuário do banco de dados.
- `DB_SENHA`: Senha do banco de dados.
- `DB_DATABASE`: Nome do banco de dados onde os dados serão importados.
- `EMAIL`, `TOKEN`, `SUBDOMAIN`: Credenciais para acessar a API de download.

---

## **Executando o Script**

Agora que o ambiente está configurado e todas as dependências foram instaladas, siga os passos abaixo para rodar o script.

### **Passo 1: Executar o script `download.py`**

Este script faz o download, descriptografa e descompacta o arquivo de backup do banco de dados.

```bash
python3 download.py
```

O script vai:

1. Limpar a pasta `dados/`.
2. Fazer a requisição à API para baixar o arquivo.
3. Descriptografar o arquivo `.gpg` usando a senha retornada pela API.
4. Descompactar o arquivo `.gz` resultante.

Após o processo, o arquivo `.sql` estará disponível na pasta `dados`.

### **Passo 2: Executar o script `banco.py`**

Após o arquivo `.sql` ser gerado, você pode importá-lo diretamente no seu banco de dados MySQL com o seguinte comando:

```bash
python3 banco.py
```

Esse script irá:

1. Ler todos os arquivos `.sql` na pasta `dados/`.
2. Importá-los automaticamente no banco de dados MySQL especificado no arquivo `.env`.

---

## **Considerações finais**

Certifique-se de que o MySQL está instalado e configurado corretamente em sua máquina. Se houver qualquer problema durante o processo de importação ou execução dos scripts, verifique os logs de erro exibidos no terminal para mais detalhes.

Se tiver dúvidas, sinta-se à vontade para consultar a documentação do MySQL ou do GnuPG.

--- 

### **Parabéns!** Agora você está pronto para executar e gerenciar o processo de download, descriptografia e importação de backups de banco de dados com sucesso!
