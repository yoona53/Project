import csv
import re
from django.core.management.base import BaseCommand
from wordle.models import Word

class Command(BaseCommand):
    help = 'Load 5~6 letter hiragana words from WLSP-basic.tsv'

    def handle(self, *args, **kwargs):
        count = 0
        with open('WLSP-basic.tsv', 'r', encoding='utf-8') as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter='\t')
            for row in reader:
                yomi = row['読み'].strip()
                if re.fullmatch(r'[ぁ-ん]{5,6}', yomi):
                    _, created = Word.objects.get_or_create(
                        text=yomi,
                        length=len(yomi),
                        defaults={'active': True}
                    )
                    if created:
                        count += 1
        self.stdout.write(self.style.SUCCESS(f"{count}個の単語を登録しました。"))
