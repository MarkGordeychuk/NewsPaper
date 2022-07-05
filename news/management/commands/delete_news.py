from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет все новости конкретной категории'
    missing_args_message = 'Category name needed'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Do you really want to delete all products? y/n')
        answer = input()

        if answer == 'y':
            try:
                Post.objects.filter(category_name=options['category']).delete()
            except Post.DoesNotExists:
                self.stdout.write(self.style.ERROR(f"Could not find category {options['category']}"))
            else:
                self.stdout.write(self.style.SUCCESS('News succesfully deleted!'))
            finally:
                return

        self.stdout.write(self.style.ERROR('Access denied'))
