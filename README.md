# Render HTMX CRUD

A tiny full-stack CRUD app built with Flask, SQLite/Postgres, Jinja templates, and HTMX.

## Features
- Create, edit, toggle, and delete tasks
- HTMX partial updates without a frontend framework
- SQLite locally, Render Postgres in production
- Ready for Git commit and Render deployment

## Run locally
```bash
python3 -m venv ~/.venv-htmx
source ~/.venv-htmx/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

Open http://127.0.0.1:5000

## Deploy to Render
1. Push this folder to a Git repository.
2. In Render, create a new Blueprint deployment from the repo.
3. Render will read `render.yaml`, create the web service and Postgres database, then deploy.

## App structure
- `app.py` - Flask app and CRUD routes
- `templates/` - Jinja pages and HTMX partials
- `render.yaml` - Render Blueprint config
