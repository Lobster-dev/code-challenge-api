# Code Challenge - API de Inscrição

Este projeto consiste em uma API para gerenciar inscrições e faixas etárias, utilizando uma arquitetura de microsserviços com FastAPI, MongoDB, e SQS (simulado com LocalStack).

## Tecnologias Utilizadas

- **Backend:** Python, FastAPI
- **Banco de Dados:** MongoDB
- **Fila de Mensagens:** AWS SQS (simulado com LocalStack)
- **Containerização:** Docker, Docker Compose
- **Testes:** Pytest

---

## 1. Configuração do Ambiente

Siga os passos abaixo para configurar o projeto localmente.

### a. Clone o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd code-challenge-api
```

### b. Crie o Arquivo de Variáveis de Ambiente

O projeto utiliza um arquivo `.env` para gerenciar as configurações. Crie uma cópia do arquivo de exemplo:

```bash
# No Windows (PowerShell)
copy .env.example .env

# No Linux ou macOS
cp .env.example .env
```

O arquivo `.env` já vem com valores padrão que funcionam para o ambiente de desenvolvimento local. Não é necessário alterá-lo para começar.

---

## 2. Executando a Aplicação

Com o Docker e o Docker Compose instalados, suba todos os serviços (API, worker, banco de dados e fila) com um único comando:

```bash
docker-compose up --build
```

- O `--build` garante que as imagens Docker serão construídas do zero na primeira vez.
- Os serviços que serão iniciados são:
  - `api`: A aplicação FastAPI, disponível em `http://localhost:8000`.
  - `worker`: O consumidor da fila SQS que processa as inscrições.
  - `mongodb`: O banco de dados MongoDB.
  - `localstack`: O simulador da AWS para o SQS.
  - `init-queue`: Um serviço temporário que cria a fila SQS assim que o LocalStack está pronto.

### Acessando a API

Após a inicialização, a documentação interativa da API (Swagger UI) estará disponível em:

**[http://localhost:8000/docs](http://localhost:8000/docs)**

Você pode usar a documentação para testar os endpoints diretamente do navegador.

**Credenciais de Autenticação (Padrão):**
- **Admin:**
  - **Usuário:** `admin`
  - **Senha:** `admin`
- **Usuário Comum:**
  - **Usuário:** `user`
  - **Senha:** `user`

---

## 3. Executando os Testes

Para rodar a suíte de testes automatizados, siga os passos abaixo.

### a. Instale as Dependências Python

É recomendado criar um ambiente virtual.

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows
.\venv\Scripts\Activate
# Linux / macOS
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### b. Inicie os Serviços em Background

Os testes de integração precisam que o banco de dados e a fila estejam ativos. Inicie os contêineres em modo "detached" (`-d`):

```bash
docker-compose up -d
```

### c. Rode o Pytest

Com os serviços rodando e as dependências instaladas, execute o Pytest (recomendado via módulo do Python):

```bash
python -m pytest -q
```

Os testes validarão os endpoints da API, a lógica de autenticação e as regras de negócio.

### Testes rápidos (mocked, sem Docker)

Os testes incluídos já usam mocks para MongoDB (`mongomock`) e SQS (mock leve). Se você só quer rodar os testes rápidos localmente sem subir o Docker, siga estes passos:

```bash
python -m venv venv
.\venv\Scripts\Activate   # Windows
pip install -r requirements.txt
python -m pytest -q
```

Isso executa a suíte de testes usando banco em memória e mocks de fila — ideal para desenvolvimento e CI.

---

## 4. Estrutura do Projeto

```
.
├── infra/                # Scripts de inicialização (ex: criar fila SQS)
├── processor/            # Lógica do worker que consome a fila
├── src/                  # Código-fonte da API
│   ├── api/              # Endpoints, schemas e lógica de autenticação
│   ├── db/               # Configuração da conexão com o MongoDB
│   └── services/         # Regras de negócio
├── tests/                # Testes automatizados
├── .env.example          # Arquivo de exemplo para variáveis de ambiente
├── docker-compose.yml    # Orquestração dos contêineres
├── Dockerfile            # Definição da imagem Docker da aplicação
└── requirements.txt      # Dependências Python
```
