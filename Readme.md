# Dados Financeiros

## Sobre o projeto

- Coletar/Tratar os dados das Ações listadas na Bolsa de Valores do Brasil(B3).
- Armazenar esses dados em um Banco de Dados para realizar consultas.
- Realizar relatórios com os dados coletados e enviar por e-mail.

## Tecnologias Utilizadas

- Python -> 3.11.5
- Banco de Dados = Postgres(13.3) -> Docker
- Consulta ao banco de dados -> DBeaver(^21.2.5)

## Site Streamlit

[Streamlit](https://dados-financeiros.onrender.com/)

## Informações

![ ](https://github.com/Prog-LucasAlves/PUB_Dados_Financeiros_B3/blob/main/Image/img01.png)

## Instalação e Configuração

1. Criando o diretório do projeto

```bash
mkdir dados_financeiros
cd dados_financeiros
```

2. Clone o repositório:

```bash
git clone https://github.com/Prog-LucasAlves/PUB_Dados_Financeiros_B3.git
```

3. Versão do Python(pyenv):

arquivo [.python-version](...)

Ref.: [pyenv](https://github.com/pyenv/pyenv)

4. Ambiente virtual(poetry)

Ref.: [poetry](https://python-poetry.org/)

5. Instalando as dependências do projeto:

```bash
poetry install
```

6. Docker

```bash
docker-compose up -d
```

Ref.: [Docker Deskyop](https://www.docker.com/products/docker-desktop/)

----
![GitHub](https://img.shields.io/github/license/Prog-LucasAlves/PUB_Dados_Financeiros_B3)
![GitHub repo size](https://img.shields.io/github/repo-size/Prog-LucasAlves/PUB_Dados_Financeiros_B3)
![GitHub top language](https://img.shields.io/github/languages/top/Prog-LucasAlves/PUB_Dados_Financeiros_B3)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/y/Prog-LucasAlves/PUB_Dados_Financeiros_B3)
![GitHub last commit](https://img.shields.io/github/last-commit/Prog-LucasAlves/PUB_Dados_Financeiros_B3)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Prog-LucasAlves/PUB_Dados_Financeiros_B3?include_prereleases)
![GitHub Release Date](https://img.shields.io/github/release-date/Prog-LucasAlves/PUB_Dados_Financeiros_B3)
![GitHub commits since latest release (by SemVer)](https://img.shields.io/github/commits-since/Prog-LucasAlves/PUB_Dados_Financeiros_B3/latest)
![GitHub issues](https://img.shields.io/github/issues/Prog-LucasAlves/PUB_Dados_Financeiros_B3)
![GitHub Repo stars](https://img.shields.io/github/stars/Prog-LucasAlves/PUB_Dados_Financeiros_B3?style=social)
![Website](https://img.shields.io/website?url=https%3A%2F%2Fdadosfinanceiros.streamlit.app%2F)
[![Linter](https://github.com/Prog-LucasAlves/PUB_Dados_Financeiros_B3/actions/workflows/linter.yml/badge.svg)](https://github.com/Prog-LucasAlves/PUB_Dados_Financeiros_B3/actions/workflows/linter.yml)
[![CodeQL](https://github.com/Prog-LucasAlves/PUB_Dados_Financeiros_B3/actions/workflows/codeql.yml/badge.svg)](https://github.com/Prog-LucasAlves/PUB_Dados_Financeiros_B3/actions/workflows/codeql.yml)
