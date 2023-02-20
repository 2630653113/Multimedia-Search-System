from django.db import models
# import os
# import django
# os.environ.setdefault('DJANGO_SETTING_MODULE', 'MultiMedia.settings')
# django.setup()


class Images(models.Model):
    location = models.CharField(max_length=1000, unique=True, verbose_name='路径', null=False)
    name = models.CharField(max_length=300, unique=True, verbose_name='图片名')
    tags = models.CharField(max_length=200, verbose_name='标签')

    def __str__(self):
        return self.location

    class Meta:
        verbose_name_plural = '图片'
