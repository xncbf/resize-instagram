import copy
import datetime
import os

from django.http import HttpResponse, JsonResponse
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
        if int(img.size[0]/4*5) > img.size[1]:
            size = (img.size[0], int(img.size[0]/4*5))
        else:
            size = (int(img.size[1]/5*4), img.size[1])
    elif ratio == '3':
        # 5:4
        if int(img.size[0]/5*4) > img.size[1]:
            size = (img.size[0], int(img.size[0]/5*4))
        else:
            size = (int(img.size[1]/4*5), img.size[1])
    layer = Image.new('RGB', size, (255,255,255))
    layer.paste(img, tuple(map(lambda x:(x[0]-x[1])//2, zip(size, img.size))))
    return layer

@task_sns
def upload_image(img, image_name, file_name):
    # upload origin image
    img.save(file_name)
    upload_file(file_name, object_name=file_name)
    os.remove(file_name)

    img.thumbnail((128,128), Image.ANTIALIAS)
    
    # upload thumbnail image
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
        results = []
        for img in imgs:
            image_name = img.name
            img = Image.open(img)
            img = upload_white_space_image(img, ratio)
            
            timestamp = int(datetime.datetime.now().timestamp()*1000000)
            file_name = f'{timestamp}{image_name}'
            upload_image(copy.deepcopy(img), image_name, file_name)
            results.append(file_name)
        return JsonResponse(results, status=201, safe=False)