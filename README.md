# ZnajomUJ

ZnajomUJ brings students at Jagiellonian University together through events that match participants in pairs. Each participant fills out a survey, which is used alongside their preferences to find a match. A built-in chat gives each pair a place to get to know each other.

*Work in progress.*

## Tech stack

- **Python** 3.13
- **Django** 5.2
- **PostgreSQL** 17
- **Docker Compose**

## Getting started

Requires Git and Docker with Compose.

```sh
git clone https://github.com/ZnajomUJ-Team/ZnajomUJ.git
cd ZnajomUJ
cp .env.example .env
```

Set `SECRET_KEY` in `.env`, then start the app:

```sh
docker compose up -d --build
docker compose exec web python manage.py migrate
```

Open [http://localhost:8000/](http://localhost:8000/).

For access to `/admin/`, create an administrator account:

```sh
docker compose exec web python manage.py createsuperuser
```

To stop the development environment without deleting database data:

```sh
docker compose down
```

## Tests

```sh
docker compose exec web python manage.py test
```

## Accounts

- The project uses a custom user model, `accounts.User` (`AUTH_USER_MODEL`). Always refer to it with
  `get_user_model()` or `settings.AUTH_USER_MODEL`, never `django.contrib.auth.models.User`.
- Users log in with their e-mail address (case-insensitive); there is no username.
- Passwords are hashed with Argon2.
- New accounts are inactive until the e-mail address is confirmed (T14). Superusers are active.
- `createsuperuser` asks for an e-mail address instead of a username.

If you ran `migrate` before the custom user model was added, reset your local database once:

```sh
docker compose down -v
docker compose up -d --build
docker compose exec web python manage.py migrate
```

## Authors

- [Julia Łapiuk](https://github.com/LapiukJulia)
- [Alicja Grzegorek](https://github.com/alicjagrzegorek)
- [Seweryn Olejnik](https://github.com/KinjeloS)
- [Jakub Karczyński](https://github.com/Kuba-kr)

## License

TBD.

## Templates and static files

- Project-wide templates live in `templates/` (`base.html`, `partials/`).
  App-specific templates live in `<app>/templates/<app>/`.
- Every page extends `base.html`. Available blocks: `title`, `extra_head`, `content`, `extra_js`.
- Static files live in `static/` (site styles in `static/css/site.css`). Use `{% static %}` in templates.
- Bootstrap 5 and HTMX are loaded from a CDN.
- Brand colours are CSS variables at the top of `static/css/site.css`.
