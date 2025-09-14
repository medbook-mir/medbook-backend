# MedBook - Медицинская информационная система

**Docker-приложение на Django + React с Celery, Redis и PostgreSQL**

## Содержание

- [Возможности](#возможности)
- [Требования](#требования)
- [Установка](#установка)
- [Запуск](#запуск)
- [Сервисы](#сервисы)
- [Celery](#celery)
- [Решение проблем](#решение-проблем)
- [Лицензия](#лицензия)

## Возможности
 **Бэкенд**: Django REST API на `http://localhost:8000`  
 **База данных**: PostgreSQL с сохранением данных  
 **Мониторинг**: Flower на `http://localhost:5555`
 **Минио**: Minio на `http://localhost:9001`

## Требования

- Docker и Docker Compose
- Python 3.9+

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-repo/medbook.git
   cd medbook
   cp .env.example .env

# Сборка и запуск
    make build

# Остановка

    make down

## Services & Ports

| Service    | URL                                            | Port | Description            |
|------------|------------------------------------------------|------|------------------------|
| Backend    | [http://localhost:8000](http://localhost:8000) | 8000 | Django REST API        |
| PostgreSQL | `host: localhost`                              | 5432 | Database               |
| Swagger     | [http://localhost:8000/swagger](http://localhost:8000/swagger) | 8000 | Swagger task api |

