from django.db import models

# Create your models here.

class Word(models.Model):
    class Meta:
        db_table = 'word_jlpt'

    expression = models.CharField(verbose_name='漢字', max_length=10)   # 漢字
    reading = models.CharField(verbose_name='ひらがな', max_length=10)         # ひらがな
    # expression = models.CharField(verbose_name='漢字', max_length=10, null=False, blank=True)   # 漢字
    # reading = models.CharField(verbose_name='ひらがな', max_length=10, null=False, blank=True)         # ひらがな
    meaning = models.CharField(verbose_name='意味', max_length=255, blank=True)
    length = models.IntegerField(verbose_name='文字数')                 # 文字数
    active = models.BooleanField(verbose_name='正解可否', default=True) # 正解可否
    tags = models.CharField(verbose_name='タグ', max_length=100, blank=True)
    

    def __str__(self):
        return f"{self.reading} ({self.expression})"
    