# crown
BTC rates in USD. 

Rates are updated every hour.

## A. setup docker

### 1. Environment
copy the content of .env.dev.docker (shared with you) to .env file (same level as 'docker-compose.yml')

### 2. Build docker container
```docker-compose up -d --build```

### 3. Get web container id
```docker ps```

### 4. create superuser on first run
```docker exec -it web_container_id python manage.py createsuperuser --username admin```

### 5. Generate token for the superuser
```docker exec -it web_container_id python manage.py drf_create_token admin```

### 6. Server
```http://127.0.0.1:8000/api/v1/quotes```

## B. API Example
```https://www.getpostman.com/collections/aee03d0eeaeb482e54cf```