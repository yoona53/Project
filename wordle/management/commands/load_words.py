import re
from django.core.management.base import BaseCommand
from wordle.models import Word

class Command(BaseCommand):
    help = 'Load 5-6 letter hiragana words from words.txt into DB'

    def handle(self, *args, **kwargs):
        count = 0
        with open('word.txt', 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                # ひらがな5~6文字単語のみフィルタリング
                if re.fullmatch(r'[ぁ-ん]{5,6}', word):
                    _, created = Word.objects.get_or_create(
                        text=word,
                        length=len(word),
                        defaults={'active': True}
                    )
                    if created:
                        count += 1
        self.stdout.write(self.style.SUCCESS(f"{count}個の単語を登録しました。"))
