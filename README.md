# Flexy Lite

Inventory management for grocery stores: a public product list with stock totals, and superuser-only screens to add, edit and delete products. Staff accounts have profiles with avatars.

## Features

- Product list with product count and total units in stock (`/`).
- Add, edit, update and delete products; only superusers can change inventory, and deleting is POST-only.
- Server-side validation (quantity cannot be negative).
- Login, logout, registration and a profile page with an avatar (resized to 300x300).
- Django admin at `/admin/`.

## Stack

Python 3.13, Django 5.2 LTS, Bootstrap 5 via django-crispy-forms, Pillow, WhiteNoise, gunicorn; SQLite by default or PostgreSQL via `DJANGO_DATABASE_URL`. Versions: [VERSIONS.md](./VERSIONS.md).

## Quickstart

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/kneeraazon404/flexy-lite.git
cd flexy-lite
uv sync --frozen
export DJANGO_DEBUG=true      # local work only; the secret key falls back to a dev value
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

The app reads real environment variables (it does not load `.env` itself); `.env.example` lists the names.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DJANGO_SECRET_KEY` | required unless `DJANGO_DEBUG=true` | startup fails without it in production |
| `DJANGO_DEBUG` | `false` | debug mode |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost` | comma-separated hosts |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | empty | comma-separated origins |
| `DJANGO_DATABASE_URL` | local SQLite file | any dj-database-url URL |
| `DJANGO_EMAIL_*` | console backend | SMTP settings |

When `DJANGO_DEBUG=false` the app enables HTTPS redirect, secure cookies and HSTS.

## Testing

```bash
uv run pytest -q
uv run ruff check . && uv run ruff format --check .
```

41 tests cover products (permissions, CRUD, totals, validation) and users (registration, login, profile). They use `flexylite.settings_test` (in-memory SQLite, temporary media). CI: `.github/workflows/ci.yml`.

## Project structure

```
flexylite/   settings, urls, wsgi/asgi, static, settings_test.py
products/    Product model, forms, views, tests
users/       profiles, auth views, signals, templates, tests
templates/   shared templates
media/       default avatar (uploads are git-ignored)
```

## Deployment

`Procfile` runs `gunicorn flexylite.wsgi:application`. Set `DJANGO_DEBUG=false`, a strong `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS` and `DJANGO_DATABASE_URL`, then run `migrate` and `collectstatic --noinput`.

## License

MIT. See `LICENSE`.
