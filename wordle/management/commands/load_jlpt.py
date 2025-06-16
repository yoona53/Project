# wordle/management/commands/import_words.py
from django.core.management.base import BaseCommand
from wordle.models import Word
import pandas as pd

def contains_katakana(text):
    return any('ァ' <= ch <= 'ヶ' for ch in str(text))

class Command(BaseCommand):
    help = 'CSV에서 단어 데이터를 불러와 Word 모델에 저장합니다.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV 파일 경로')
    
    def handle(self, *args, **options):
        csv_path = options['csv_file']
        df = pd.read_csv(csv_path)

        Word.objects.all().delete()
        self.stdout.write(self.style.WARNING('기존 Word 데이터가 모두 삭제되었습니다.'))

        count = 0
        for _, row in df.iterrows():
            expression = row['expression']
            reading = row['reading']
            meaning = row.get('meaning', '')
            tags = row['tags']            
            length = len(str(reading))

            # print(f"{expression} / {reading} / {tags}")

            if not expression or not reading or contains_katakana(reading):
                continue

            Word.objects.create(
                expression=expression,
                reading=reading,
                meaning=meaning,
                length=length,
                active=True,
                tags=tags
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'{count}개의 단어가 성공적으로 삽입되었습니다.'))
