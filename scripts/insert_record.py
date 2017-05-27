# coding=utf-8
import time
import re
from openpyxl import load_workbook
from scripts.yuntu_doc import *


# 在mongodb中，把Course转换为MediaAlbum



# 16953



def delete_media_album():
    count = 0
    for i in MediaAlbum.objects(source='网易云课堂'):
        es.delete('media-album-index', 'media-album', str(i.id))
        i.delete()
        count += 1
        print count


def delete_media():
    count = 0
    for i in Media.objects(timeline__gt=1493307600000):
        i.delete()
        count += 1
        print count


def delete_album_by_id(id):
    MediaAlbum.objects.get(id=id).delete()
    es.delete('media-album-index', 'media-album', id)


def modify_cover():
    count = 0
    for i in Media.objects(timeline__gt=1493307600000):
        obj = re.search(r'imgurl=(http:.*\.jpg)_140x80x1x95.jpg', i.cover if i.cover else '')
        if obj:
            i.update(cover=obj.group(1))
            count += 1
            print count


def modify_label(media_album):
    label1 = 230000
    if 'TED' in media_album.tags:
        label2 = 230100
    else:
        label2 = 230200
    media_album.update(label1=label1, label2=label2, open=1)
