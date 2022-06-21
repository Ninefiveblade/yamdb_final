# Проект yamdb_final

![example workflow](https://github.com/Ninefiveblade/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

#### API проект, на котором вы можете обозревать различные фильмы, музыку, кино.
#### Проект позволяет общаться друг с другом через систему review и комментариев.
#### Каждое произведение имеет систему оценки, исходяющию из отзывов.
#### Теперь пользователи могут быстро выбрать понравившееся кино, музыку или еще что-то творческое!

#### Автор: Иван, Яндекс Практикум.
#### Технологии: Django REST, Docker, JWT, Python 3.6.7

## Установить проект:

```git clone git@github.com:Ninefiveblade/api_yamdb.git```

## Наполнение .env path (your_path/infra/.env)

```
ALLOWED_HOSTS = "Your hosts"
SECRET_KEY = "Your secret key"
ENTER_PASS = "Your email Email SMTP PASS"

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD= "your passeord"
DB_HOST="your container name"
DB_PORT=5432 
```

## Запуск тестов:

#### Из корневой папки проета:

```pytest```

## Запустить проект:

```your_path/infra/docker-compose up -d```

## Выполнить миграции:

```docker-compose exec web python manage.py makemigrations```
```docker-compose exec web python manage.py migrate```

## Создать суперпользователя:

```docker-compose exec web python manage.py createsuperuser```

## Собрать статику для корректного отображения страниц:

```docker-compose exec web python manage.py collectstatic --no-input```

## Заполнить базу данных:

```docker-compose exec web python manage.py update```

## Документация:

```http://127.0.0.1:8000/redoc```

## Пример запроса:
#### Получить все произведения:

```http://127.0.0.1:8000/api/v1/titles/```

## Зарегистрироваться:

```http://127.0.0.1:8000/api/v1/auth/signup/```

## Получить токен:
```http://127.0.0.1:8000/api/v1/auth/token/```

## Сохранить дамп базы данных:

```docker-compose exec web python manage.py dumpdata > fixtures.json```

## License

[LICENSE MIT](LICENSE.md)
