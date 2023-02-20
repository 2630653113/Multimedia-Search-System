if __name__ == '__main__':
    import os
    import django

    os.environ.setdefault('DJANGO_SETTING_MODULE', 'MultiMedia.settings')
    django.setup()
    from SearchSystem.models import Images

    path = 'D:\PythonProjects\pythonProject\Image\\'
    image_list = os.listdir(path)
    for image in image_list:
        image_record = Images(location=path + image, name=image, tags=image.replace('.jpg', ''))
        image_record.save()
        print('ok!')