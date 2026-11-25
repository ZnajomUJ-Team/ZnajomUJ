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

TBD.

## Authors

- [Julia Łapiuk](https://github.com/LapiukJulia)
- [Alicja Grzegorek](https://github.com/alicjagrzegorek)
- [Seweryn Olejnik](https://github.com/KinjeloS)
- [Jakub Karczyński](https://github.com/Kuba-kr)

## License

TBD.
