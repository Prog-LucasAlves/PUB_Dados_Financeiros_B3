# Stage 1: Build virtual environment with uv
FROM python:3.11-slim AS builder

WORKDIR /app

# Instala uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copia as especificações de dependências
COPY pyproject.toml uv.lock ./

# Sincroniza as dependências em modo freeze (sem pacotes de desenvolvimento)
RUN uv sync --frozen --no-dev --no-install-project

# Stage 2: Runtime image
FROM python:3.11-slim AS runner

WORKDIR /app

# Cria um usuário não-root por motivos de segurança e boas práticas
RUN groupadd -r streamlit && useradd -r -g streamlit streamlit

# Copia o ambiente virtual compilado e o código-fonte do projeto
COPY --from=builder /app/.venv /app/.venv
COPY . /app

# Configura caminhos e variáveis de ambiente
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Altera a permissão dos arquivos para o usuário seguro
RUN chown -R streamlit:streamlit /app

USER streamlit

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py"]
