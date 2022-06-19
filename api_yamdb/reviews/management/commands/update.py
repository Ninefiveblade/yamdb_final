"""Файл загрузки даных в базу данных проекта."""
import csv

from django.core.management.base import BaseCommand
from django.conf import settings

from reviews import models
from users.models import YamDBUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            with open(
                f'{settings.STATICFILES_DIRS[0]}data/category.csv'
            ) as table:
                reader = csv.DictReader(table)
                models.Category.objects.all().delete()
                for row in reader:
                    models.Category.objects.get_or_create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                print('Category upload ready')
            with open(
                f'{settings.STATICFILES_DIRS[0]}data/genre.csv'
            ) as table:
                reader = csv.DictReader(table)
                models.Genre.objects.all().delete()
                for row in reader:
                    models.Genre.objects.get_or_create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
                print('Genre upload ready')
            with open(
                f'{settings.STATICFILES_DIRS[0]}data/titles.csv'
            ) as table:
                reader = csv.DictReader(table)
                models.Title.objects.all().delete()
                for row in reader:
                    models.Title.objects.get_or_create(
                        id=row['id'],
                        name=row['name'],
                        year=row['year'],
                        category_id=row['category']
                    )
                print('Title upload ready')
            with open(
                f'{settings.STATICFILES_DIRS[0]}data/genre_title.csv'
            ) as table:
                reader = csv.DictReader(table)
                models.Title.genre.through.objects.all().delete()
                for row in reader:
                    models.Title.genre.through.objects.get_or_create(
                        id=row['id'],
                        title_id=row['title_id'],
                        genre_id=row['genre_id']
                    )
                print('GenreTitle upload ready')
            with open(
                f'{settings.STATICFILES_DIRS[0]}data/users.csv'
            ) as table:
                reader = csv.DictReader(table)
                YamDBUser.objects.all().delete()
                for row in reader:
                    YamDBUser.objects.get_or_create(
                        id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name']
                    )
                print('YamDBUser upload ready')
            with open(
                f'{settings.STATICFILES_DIRS[0]}data/review.csv'
            ) as table:
                reader = csv.DictReader(table)
                models.Review.objects.all().delete()
                for row in reader:
                    models.Review.objects.get_or_create(
                        id=row['id'],
                        text=row['text'],
                        title_id=row['title_id'],
                        pub_date=row['pub_date'],
                        score=row['score'],
                        author_id=row['author'],
                    )
                print('Review upload ready')
            with open(
                f'{settings.STATICFILES_DIRS[0]}data/comments.csv'
            ) as table:
                reader = csv.DictReader(table)
                models.Comment.objects.all().delete()
                for row in reader:
                    models.Comment.objects.get_or_create(
                        id=row['id'],
                        text=row['text'],
                        pub_date=row['pub_date'],
                        review_id=row['review_id'],
                        author_id=row['author'],
                    )
                print('Comment upload ready')
            print('everything up-to-date')
        except Exception as er:
            print('Something wrong with your db, '
                  'or migration, please check it, '
                  f'error: {er}')
