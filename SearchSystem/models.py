from django.db import models


class Images(models.Model):
    location = models.CharField(max_length=1000, unique=True, verbose_name='路径', null=False)
    name = models.CharField(max_length=50, unique=True, verbose_name='图片名')
    tags = models.CharField(max_length=50, verbose_name='标签')

    def __str__(self):
        return self.location

    class Meta:
        verbose_name_plural = '图片'


class Music(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='音频名')
    location = models.CharField(max_length=1000, unique=True, verbose_name='路径', null=False)
    tag = models.IntegerField(default=0, verbose_name='标签')

    def __str__(self):
        return self.location

    class Meta:
        verbose_name_plural = '音频'
