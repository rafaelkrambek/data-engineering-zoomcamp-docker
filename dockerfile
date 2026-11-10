FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvbin/

# Adiciona o uv e o ambiente virtual gerado ao PATH
ENV PATH="/code/.venv/bin:/uvbin:$PATH"

WORKDIR /code

# Copia os arquivos de configuração de dependências
COPY pyproject.toml .python-version uv.lock ./

# Instala as dependências no .venv (/code/.venv)
RUN uv sync --frozen --no-dev --no-install-project

# Copia o script de ingestão
COPY ingest_data.py .

# Como o PATH já aponta para o .venv, basta chamar python diretamente
ENTRYPOINT ["python", "ingest_data.py"]