import os
import boto3
import copy
import datetime
import logging
import io
import os

from datetime import date

from PIL import Image, ImageFile

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
    # img.thumbnail((800,800), Image.ANTIALIAS)
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
    layer.paste(img, tuple(map(lambda x:(x[0]-x[1])//2, zip(size, img.size))), img)
    return layer

def upload_image(img, file_name, s3_file_path):
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
    upload_file('/tmp/'+file_name, object_name=s3_file_path+file_name)
    
    # upload thumbnail image
    upload_file('/tmp/th_' + file_name, object_name='thumbnail/'+file_name)

def upload_white_space_image(img, ratio):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    content_type = img.content_type.split('/')[1]
    print("img.content_type: %s" % img.content_type)
    print("img.file: %s" % img.file)
    print("img.file.name: %s" % img.file.name)
    print("img.file.mode: %s" % img.file.mode)
    print("img.file.tell(): %s" % img.file.tell())
    data = img.file.read()
    print(len(data))
    print(data[:40])
    img = Image.open(img.file)
    img = img.convert("RGBA")
    timestamp = int(datetime.datetime.now().timestamp()*1000000)
    file_name = f'{timestamp}.{content_type}'
    today = date.today()
    s3_file_path=f'{today.year}/{today.month}/{today.day}/'
    img = get_white_square(img, ratio)
    upload_image(img, file_name, s3_file_path)
    return s3_file_path + file_name

def upload_file(file_name, bucket="resize-media", object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')
    s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL':'public-read'})
    os.remove(file_name)
