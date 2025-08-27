# ALX Backend — Caching Property Listings

A Django REST-style mini-service demonstrating layered caching for property listings using Redis via django-redis. It exposes endpoints to fetch property listings (with caching) and to view Redis cache metrics (hits/misses/hit ratio). Includes Docker Compose services for PostgreSQL and Redis.


## Features
- Property model (title, description, price, location, created_at).
- GET /properties/ returns all properties.
  - View-level caching with cache_page for 15 minutes.
  - Data-level caching of the queryset for 1 hour in Redis (key: all_properties).
  - Automatic cache invalidation on create/update/delete via Django signals.
- GET /properties/cache_metrics/ exposes Redis keyspace hit/miss counts and hit ratio.
- Docker Compose services for Postgres and Redis.


## Tech Stack
- Python 3.12+
- Django 5.2
- Redis (via django-redis)
- PostgreSQL
- python-decouple for environment variables
- Docker Compose (optional, for services)


## Project Layout
- alx_backend_caching_property_listings/settings.py — Django settings (Postgres + Redis cache).
- properties/models.py — Property model.
- properties/views.py — property_list and cache_metrics endpoints.
- properties/utils.py — caching helpers and Redis metrics.
- properties/signals.py — invalidates all_properties cache on save/delete.
- properties/management/commands/create_db.py — convenience command to create the database if missing.
- docker-compose.yml — Redis and Postgres services.


## Prerequisites
- Python 3.12+
- Redis (local or via Docker)
- PostgreSQL (local or via Docker)
- Recommended: virtual environment manager


## Quick Start
You can run Postgres and Redis with Docker, and run Django on your host machine.

1. Start Postgres and Redis
   - Create a .env file in the project root (next section shows variables).
   - Run: docker compose up -d

2. Create the database (optional helper)
   - With the Docker services running, in another terminal run:
     - python manage.py create_db

3. Install dependencies
   - Using pip:
     - python -m venv .venv
     - source .venv/bin/activate  (on Windows: .venv\\Scripts\\activate)
     - python -m pip install -U pip
     - pip install -e .  (or: pip install -r requirements)
     
     This project declares dependencies in pyproject.toml, so pip will read them when using -e .

   - Or using uv (if installed):
     - uv sync

4. Apply migrations
   - python manage.py migrate

5. Create a superuser (optional, to use Django Admin)
   - python manage.py createsuperuser

6. Run the server
   - python manage.py runserver
   - Open: http://127.0.0.1:8000/properties/
   - Metrics: http://127.0.0.1:8000/properties/cache_metrics/


## Environment Variables (.env)
The project uses python-decouple, so define these in a .env file at the repository root:

- POSTGRES_DB=listings_db
- POSTGRES_USER=your_user
- POSTGRES_PASSWORD=your_password
- POSTGRES_DB_HOST=localhost
- POSTGRES_DB_PORT=5432

Notes:
- If you run Django on your host and Postgres via Docker Compose, the host should be localhost because the port 5432 is published to the host.
- Redis is configured at redis://127.0.0.1:6379 in settings.py by default. If you change your Redis host/port, update settings.py accordingly.


## API Endpoints
- GET /properties/
  - Returns JSON with all properties.
  - Example response:
    {
      "properties": [
        {"id": 1, "title": "Cozy Studio", "description": "...", "price": "800.00", "location": "Nairobi", "created_at": "2025-08-27T12:34:56Z"},
        {"id": 2, "title": "2BR Apartment", ...}
      ]
    }
  - Caching:
    - Django view cache for 15 minutes.
    - Redis cache for the queryset for 1 hour under key all_properties.
    - Cache invalidates automatically on Property save/delete via signals.

- GET /properties/cache_metrics/
  - Returns Redis keyspace metrics:
    {"hits": <int>, "misses": <int>, "hit_ratio": <float>}
  - If Redis is unavailable, returns {"error": "..."}.


## Creating Sample Data
You can create data via Django Admin or the shell:

- Admin: http://127.0.0.1:8000/admin/ (after createsuperuser)
- Shell:
  - python manage.py shell
  - from properties.models import Property
  - Property.objects.create(title="Cozy Studio", description="Near CBD", price=800, location="Nairobi")

After adding/updating/deleting Property instances, the all_properties cache key is cleared by signals so the next request will refresh the cache.


## How Caching Works Here
- View-level cache (cache_page(60*15)) wraps the property_list endpoint, so identical GET requests within 15 minutes return the cached response without hitting the view.
- Data-level cache in properties/utils.get_all_properties caches the queryset (Property.objects.all()) for 1 hour in Redis.
- Signals (post_save/post_delete) delete the all_properties key to keep cached data fresh.
- Redis metrics are read from INFO to compute hits, misses, and simple hit_ratio.


## Running Tests
- Currently, no functional tests are defined beyond the default scaffold.
- You can still run the test runner:
  - python manage.py test


## Troubleshooting
- psycopg2 connection errors:
  - Ensure docker compose services are up and env vars match docker-compose.yml.
  - Verify you can connect: psql -h localhost -p 5432 -U $POSTGRES_USER -d listings_db
- Redis metrics error or hit_ratio division issues:
  - Ensure Redis is running (docker compose up -d redis) and reachable at 127.0.0.1:6379.
- Migrations fail due to missing DB:
  - Run python manage.py create_db first , then migrate.
- CORS/Hosts in production:
  - Update ALLOWED_HOSTS in settings.py as appropriate for deployment.


## License
- MIT
