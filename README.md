## Environment Requirements

1. This application was built against Python 3.6
2. Postgres 9.4 and above, running locally on port 5432

## Environment Variables

This project uses python-dotenv to autoload environment variables from `.env` files

```
FLASK_APP='app'
FLASK_ENV='development'
DATABASE_URL="postgres://localhost:5432/instagram"
SECRET_KEY="secretkey"
```

## To Setup

```bash
pip install -r requirements.txt
flask db upgrade
```

## To run server with environment variables loaded

```bash
flask run
```

## To run shell with environment variables loaded
```bash
flask shell
```

## WARNING

This repository comes with `.env` file for use with `python-dotenv`. Remember to avoid commiting `.env` files or any files that may contain environment variables or sensitive data such as api keys in repositories.

The `.env` is added here only for educational purposes.
