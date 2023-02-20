from haystack import indexes
from .models import Images


class ImagesIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Images索引数据模型类
    """
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    location = indexes.CharField(model_attr='location')

    def get_model(self):
        """返回建立索引的模型类"""
        return Images

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.all()