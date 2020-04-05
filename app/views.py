import copy
import datetime
import io
import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from PIL import Image

from app.utils import async_upload_file

RATIO_TUPLE = (
    (1, '1:1'),
    (2, '4:5'),
    (3, '5:4')
)

def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format='PNG')
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


def get_white_square(img, ratio):
    img.thumbnail((800,800), Image.ANTIALIAS)
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

def upload_image(img, image_name, file_name):
    # stream byte
    # byte_img = image_to_byte_array(img)
    # img.thumbnail((128,128), Image.ANTIALIAS)
    # byte_th_img = image_to_byte_array(img)
    # save file
    th = copy.deepcopy(img)
    th.thumbnail((128,128), Image.ANTIALIAS)
    img.save('/tmp/'+file_name)
    img.thumbnail((128,128), Image.ANTIALIAS)
    img.save('/tmp/th_' + file_name)
    # upload origin image
    async_upload_file('/tmp/'+file_name, object_name=file_name)
    
    # upload thumbnail image
    async_upload_file('/tmp/th_' + file_name, object_name='thumbnail/'+file_name)

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
            upload_image(img, image_name, file_name)
            results.append(file_name)
        return JsonResponse(results, status=201, safe=False)