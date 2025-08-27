from django.core.management.base import BaseCommand
import psycopg2
from psycopg2 import sql
from decouple import config


class Command(BaseCommand):
    help = "Check if PostgreSQL database exists, create it if not."

    def handle(self, *args, **options):
        db_name = config('POSTGRES_DB')
        db_user = config('POSTGRES_USER')
        db_password = config('POSTGRES_PASSWORD')
        db_host = config('POSTGRES_DB_HOST', default='localhost')
        db_port = config('POSTGRES_DB_PORT', default='5432')

        try:
            # Connect to default 'postgres' db
            conn = psycopg2.connect(
                dbname="postgres",
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            conn.autocommit = True
            cur = conn.cursor()

            # Check if DB exists
            cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (db_name,))
            exists = cur.fetchone()

            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                self.stdout.write(self.style.SUCCESS(f"✅ Database '{db_name}' created"))
            else:
                self.stdout.write(self.style.WARNING(f"ℹ️ Database '{db_name}' already exists"))

            cur.close()
            conn.close()

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error: {e}"))
