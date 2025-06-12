# wordle/management/commands/load_jlpt.py
import csv
from django.core.management.base import BaseCommand
from wordle.models import Word

class Command(BaseCommand):
    help = 'elzup jlpt-word-list N1-N5 All Vocabulary List'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path', '-p', default='jlpt-word-list\out\all.csv',
            help='CSV ファイルパス'
        )

    def handle(self, *args, **options):
        path = options['path']
        self.stdout.write(f"Loading from {path} …")

        # 既存データの初期化
        Word.objects.all().delete()

        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                expr = row.get('expression') or row.get('表現')
                read = row.get('reading')    or row.get('読み')
                if not expr or not read:
                    continue

                # readingの長さの指定(例：5〜6文字だけ選んで入れたい場合は、以下のifを使う)
                if len(read) not in (5,6):
                    continue

                Word.objects.create(
                    expression=expr,
                    reading=read,
                    length=len(read),
                    active=True
                )

        self.stdout.write(self.style.SUCCESS('✅ JLPTワードローディング完了'))
