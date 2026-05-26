# 🚀 Guia de Onboarding & Setup Local: Neo-B3 Obsidian

Bem-vindo ao projeto **Neo-B3 Obsidian**! Este guia descreve o processo passo a passo para configurar o ambiente de desenvolvimento local, validar a qualidade do código com o linter Ruff e executar as suítes de testes automatizados de forma ágil e segura usando a ferramenta `uv`.

---

## 1. Pré-requisitos

Certifique-se de possuir instalado em sua máquina:
* **Python 3.11.x** (a versão principal utilizada pelo projeto é a 3.11.5).
* **Git** para versionamento de código.
* **Astral uv** (gerenciador de dependências e ambientes Python de alto desempenho).
  * *Para instalar o `uv` no Windows (PowerShell):*
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
  * *Para instalar o `uv` no Linux/macOS:*
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

---

## 2. Configurando o Ambiente Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Prog-LucasAlves/PUB_Dados_Financeiros_B3.git
   cd PUB_Dados_Financeiros_B3
   ```

2. **Crie e sincronize o ambiente virtual (`.venv`):**
   O `uv` sincronizará de forma congelada e ultra veloz todas as dependências especificadas nos arquivos `pyproject.toml` e `uv.lock`:
   ```bash
   uv sync --frozen
   ```

3. **Carregue as variáveis de ambiente:**
   Duplique o arquivo de variáveis de ambiente de exemplo (caso exista) ou crie o arquivo `.env` na raiz do projeto com as credenciais locais do PostgreSQL:
   ```env
   DB_USER=root
   DB_PASSWORD=root
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=b3_database
   ```

---

## 3. Rodando o Streamlit localmente

Para visualizar o painel interativo financeiro "Neo-B3 Obsidian" no navegador, execute o comando:
```bash
uv run streamlit run app.py
```
O Streamlit abrirá automaticamente uma aba no navegador no endereço local: [http://localhost:8501](http://localhost:8501).

---

## 4. Garantindo a Qualidade do Código

Nossos padrões de linting e formatação de código são validados de forma ágil utilizando o **Ruff**:

* **Verificar erros e problemas de linter:**
  ```bash
  uv run ruff check .
  ```

* **Formatação automática do código:**
  ```bash
  uv run ruff format .
  ```

* **Validação de Formatação (apenas check sem alterar arquivos):**
  ```bash
  uv run ruff format --check .
  ```

---

## 5. Executando a Suíte de Testes

Os testes de integração e unitários estão localizados na pasta `tests/` e são executados de forma limpa usando a engine `pytest`:

* **Rodar toda a suíte de testes:**
  ```bash
  uv run pytest
  ```

* **Rodar testes exibindo prints e logs de execução:**
  ```bash
  uv run pytest -s
  ```

---

## 6. Pre-Commit Hooks

O projeto possui validação local antes de cada commit para evitar que códigos mal-formatados ou com erros subam para o repositório. Ative os hooks locais executando:
```bash
uv run pre-commit install
```
A partir de agora, toda vez que rodar `git commit`, os arquivos modificados serão formatados e analisados automaticamente.
