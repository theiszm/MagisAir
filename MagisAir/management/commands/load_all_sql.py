from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    "Loads all .sql files from the sql/ folder (alphabetical order)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default="sql",
        )

    def handle(self, *args, **options):
        folder = Path(options["path"])

        if not folder.exists():
            self.stderr.write(self.style.ERROR(f"Folder not found: {folder}"))
            return

        sql_files = sorted(folder.glob("*.sql"))

        if not sql_files:
            self.stdout.write(self.style.WARNING("No .sql files found."))
            return

        self.stdout.write(self.style.SUCCESS(f"Found {len(sql_files)} SQL files."))

        with connection.cursor() as cursor:
            for file in sql_files:
                self.stdout.write(self.style.HTTP_INFO(f"\nRunning: {file.name}"))

                sql_text = file.read_text(encoding="utf-8")

                # Split into individual SQL statements by semicolon
                statements = sql_text.split(";")

                for i, raw_stmt in enumerate(statements, start=1):
                    stmt = raw_stmt.strip()
                    if not stmt:
                        continue
                    try:
                        cursor.execute(stmt)
                    except Exception as e:
                        self.stderr.write(
                            self.style.ERROR(f"Error in {file.name}, statement {i}: {e}")
                        )
                        raise

                self.stdout.write(self.style.SUCCESS(f"✓ Completed: {file.name}"))

        self.stdout.write(self.style.SUCCESS("\nALL SQL FILES EXECUTED SUCCESSFULLY."))

