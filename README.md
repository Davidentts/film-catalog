# Film catalog

[![Python Checks](https://img.shields.io/github/actions/workflow/status/Davidentts/film-catalog/python-checks.yaml?branch=master&style=for-the-badge&logo=githubactions&logoColor=white&label=Python%20Checks)](https://github.com/Davidentts/film-catalog/actions/workflows/python-checks.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge&logo=python&logoColor=white)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/lint-ruff-D7FF64?style=for-the-badge&logo=ruff&logoColor=black)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/type%20checking-mypy-2A6DB2?style=for-the-badge&logo=python&logoColor=white)](https://github.com/python/mypy)
[![uv](https://img.shields.io/badge/package%20manager-uv-DE5FE9?style=for-the-badge&logo=astral&logoColor=white)](https://github.com/astral-sh/uv)
[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge)](https://github.com/pre-commit/pre-commit)

## Develop

### Setup

Right click 'film-catalog-source' -> Mark directory as -> Sources Root

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Install

Install packages:
```shell
uv sync
```

### Run

Go to work dir
```shell
cd film-catalog-source
```

Run dev sever
```shell
fastapi dev
```

## Snippets

```shell
python -c 'import secrets;print(secrets.token_urlsafe(16))'
```
