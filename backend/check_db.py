import os
import psycopg2
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            print(" Database connection successful!")
            conn.close()
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise