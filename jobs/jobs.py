from django.conf import settings
import os
import time


def clean_media():
    filenames = os.listdir(settings.MEDIA_ROOT)
    now = time.time()
    for filename in filenames:
        if now - os.path.getatime(os.path.join(settings.MEDIA_ROOT, filename)) > 100:
            print(os.path.join(settings.MEDIA_ROOT, filename))
            os.remove(os.path.join(settings.MEDIA_ROOT, filename))
