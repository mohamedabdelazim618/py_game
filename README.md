# Vault Access PIN Game

A small Flask web game where players guess a randomly generated four-digit PIN and receive points for exact and misplaced digits.

## Requirements

- Python 3.10 or newer
- `pip`

## Run locally

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and start the app:

```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Environment variables

Copy `.env.example` to `.env` for local configuration if needed. Do not commit `.env` or place real secrets in this README.

- `SECRET_KEY`: Flask session signing key. Use a long random value in production.
- `PORT`: Optional local port. Render provides this automatically.

The app includes a development fallback for `SECRET_KEY`, but production deployments must set a real secret through the hosting provider.

## Deploy on Render

This repository includes `render.yaml` for a Render Blueprint deployment.

1. Push the project to a Git repository.
2. In Render, choose **New > Blueprint**.
3. Select the repository and approve the detected `render.yaml`.
4. Render installs `requirements.txt` and starts the app with `gunicorn app:app`.
5. Confirm that `SECRET_KEY` is configured as a generated secret in the Render service environment.

The service does not require a database. Scores are stored in the user's Flask session cookie.

## Project structure

```text
app.py                 Flask application
requirements.txt       Python dependencies
render.yaml            Render deployment configuration
.env.example           Safe environment variable template
static/                CSS and browser JavaScript
templates/             HTML templates
```

## Security notes

- Never commit `.env`, API keys, passwords, or production secrets.
- Use Render's generated `SECRET_KEY` value in production.
- Do not enable Flask debug mode in production.
