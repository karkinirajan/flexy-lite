# Flexy Lite

## Overview

Flexy Lite is an inventory management application for grocery operations. It uses Django with environment-driven configuration, a responsive Bootstrap 5 UI, and uv for dependency and environment management.

## Stack

- Backend: Django + Python
- Frontend: HTML, CSS, Bootstrap 5
- Dependency and environment management: uv (`pyproject.toml` + `uv.lock`)

## Prerequisites

- Python 3.12+
- uv (<https://docs.astral.sh/uv/getting-started/installation/>)

## Quick Start (uv)

1. Clone and enter the project:

    ```bash
    git clone https://github.com/kneeraazon404/flexy-lite.git
    cd flexy-lite
    ```

2. Create or refresh the local virtual environment and install from lock:

    ```bash
    uv venv .venv
    uv sync --frozen
    ```

3. Create local environment variables:

    ```bash
    cp .env.example .env
    ```

4. Run database setup and start development server:

    ```bash
    uv run python manage.py migrate
    uv run python manage.py runserver
    ```

## Environment Variables

Use `.env.example` as the source of truth. Important keys:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_DATABASE_URL`
- `DJANGO_EMAIL_*`

## Common uv Commands

- Install/update environment from project metadata:

   ```bash
   uv sync
   ```

- Add a dependency:

   ```bash
   uv add <package>
   ```

- Remove a dependency:

   ```bash
   uv remove <package>
   ```

- Update lockfile after dependency changes:

   ```bash
   uv lock
   ```

- Run Django checks:

   ```bash
   uv run python manage.py check
   ```

## Deployment Notes

- Set production-safe values:
  - `DJANGO_DEBUG=false`
  - strong `DJANGO_SECRET_KEY`
  - valid `DJANGO_ALLOWED_HOSTS`
  - valid `DJANGO_CSRF_TRUSTED_ORIGINS`
- Ensure static collection runs during deploy:

   ```bash
   uv run python manage.py collectstatic --noinput
   ```

- Process command is configured in `Procfile`:

   ```bash
   web: gunicorn flexylite.wsgi:application --log-file -
   ```

## License

This project is licensed under the MIT License. See `LICENSE` for details.
