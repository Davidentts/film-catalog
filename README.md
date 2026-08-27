# Film catalog

[![Python checks 🐍](https://github.com/Davidentts/film-catalog/actions/workflows/python-checks.yaml/badge.svg)](https://github.com/Davidentts/film-catalog/actions/workflows/python-checks.yaml)

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
