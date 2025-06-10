from django.db import models

# Create your models here.

class Word(models.Model):
    class Meta:
        db_table = 'word'

    text = models.CharField(verbose_name='単語', max_length=10)
    length = models.IntegerField(verbose_name='文字数')
    active = models.BooleanField(verbose_name='正解可否', default=True)

    def __str__(self):
        return self.text