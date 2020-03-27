import datetime
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from PIL import Image
from zappa.asynchronous import task_sns

from app.utils import upload_file

RATIO_TUPLE = (
    (1, '1:1'),
    (2, '4:5'),
    (3, '5:4')
)


def get_thumbnail(img):
    return img.resize((100, 100), Image.ANTIALIAS)

def get_white_big_square(img):
    "return a white-background-color image having the img in exact center"
    size = (max(img.size),)*2
    layer = Image.new('RGB', size, (255,255,255))
    layer.paste(img, tuple(map(lambda x:(x[0]-x[1])//2, zip(size, img.size))))
    return layer

@task_sns
def upload_white_space_image(img, ratio):
    try:
        img = get_white_big_square(img)
        timestamp = int(datetime.datetime.now().timestamp()*1000000)
        file_name = f'{timestamp}.jpg'
        img.save(file_name)
        upload_file(file_name)
        os.remove(file_name)
    except Exception as e:
        pass
    return HttpResponse(status=503)
    
class IndexView(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        imgs = request.FILES.getlist('images')
        ratio = request.POST['ratio']
        for img in imgs:
            img = Image.open(img)
            upload_white_space_image(img, ratio)
        return HttpResponse(status=201)