# travelperk-api

## Technologies Used:
This project uses `asynchronous programming` with the help of following technologies:

- [FastAPI](https://github.com/tiangolo/fastapi)
- [Python AsyncIO](https://docs.python.org/3/library/asyncio.html)
- PostgreSQL
- [databases](https://github.com/encode/databases) (async support for database)
- [SQL Alchemy Core](https://docs.sqlalchemy.org/en/14/core/) (DB Driver)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) (DB migration tool)   
- [httpx](https://github.com/encode/httpx) (async http client)   
- [uvicorn](https://github.com/encode/uvicorn) (ASGI server)
- Swagger API docs  
- Pytest


### Style guide, Formatters and linters used

- [Black](https://github.com/psf/black) (as formatter)
- [Flake8](https://flake8.pycqa.org/en/latest/) (PEP8 Style Guide Enforcer)
- [Pre-commit](https://github.com/pre-commit/pre-commit)  (Pre commit hooks Runner)
- [Mypy](https://github.com/python/mypy) (static type checker)


## Instructions

### Running development server

```bash
make run_dev
```

### Running tests

```bash
make test
```

## API testing guideline
### Using Swagger UI
Browse [Swagger Doc](http://127.0.0.1:8080/docs)
