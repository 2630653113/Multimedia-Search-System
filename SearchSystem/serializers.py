from drf_haystack.serializers import HaystackSerializer


class ImagesIndexSerializer(HaystackSerializer):
    """
    索引结果数据序列化器
    """

    class Meta:
        index_classes = [ImagesIndex]
        fields = ('text', 'id', 'name', 'location')