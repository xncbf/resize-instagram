import copy
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

def get_white_square(img, ratio):
    max_size = max(img.size)
    """return a white-background-color image having the img in ratio"""
    if ratio == '1':
        # 1:1
        size = (max_size, )*2
    elif ratio == '2':
        # 4:5
        size = (max_size, max_size/4*5)
    elif ratio == '3':
        # 5:4
        size = (max_size/4*5, max_size)    
    layer = Image.new('RGB', size, (255,255,255))
    layer.paste(img, tuple(map(lambda x:(x[0]-x[1])//2, zip(size, img.size))))
    return layer

@task_sns
def save_thumbnail(img, image_name):
    timestamp = int(datetime.datetime.now().timestamp()*1000000)
    file_name = f'{timestamp}{image_name}'
    img.thumbnail((128,128), Image.ANTIALIAS)
    img.save(file_name)
    upload_file(file_name, object_name='thumbnail/'+file_name)
    os.remove(file_name)

def upload_white_space_image(img, ratio):
    return get_white_square(img, ratio)
    
class IndexView(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        imgs = request.FILES.getlist('images')
        ratio = request.POST['ratio']
        for img in imgs:
            image_name = img.name
            img = Image.open(img)
            img = upload_white_space_image(img, ratio)
            _img = copy.deepcopy(img)
            save_thumbnail(_img, image_name)
        return HttpResponse(status=201)