if __name__ == '__main__':
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MultiMedia.settings')
    django.setup()
    from SearchSystem.models import Music, Images

    class_mapping = {
        0: 'blues',
        1: 'classical',
        2: 'country',
        3: 'disco',
        4: 'hiphop',
        5: 'jazz',
        6: 'metal',
        7: 'pop',
        8: 'reggae',
        9: 'rock'
    }

    root_path = 'D:\PythonProjects\MultiMedia\Source\music\\'
    for index in range(10):
        path = root_path + class_mapping[index] + '\\'
        music_list = os.listdir(path)
        for music in music_list:
            music_record = Music(name=music, location=path + music,  tag=index)
            music_record.save()
            print('%d ok!' % index)
