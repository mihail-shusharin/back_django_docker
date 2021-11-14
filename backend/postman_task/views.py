import re
from http.client import HTTPResponse

from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
from django.shortcuts import render, redirect
from postman_task.models import Image as Im
from rest_framework import status
from rest_framework.response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from postman_task.forms import ImageForm
from config import settings
import requests
from PIL import Image as pil_img
import io
import json
# Create your views here.


class ImageView(APIView):
    def post(self, request):
        try:
            file = request.FILES['file']
            pil_im = pil_img.open(file)
            width, height = pil_im.size
            img_obj = Im.objects.create(image_file=file, widht=width, height=height)
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            url = request.data.get('url')
            if url is not None:
                data = requests.get(url, stream=True).content
                tmpFile = pil_img.open(io.BytesIO(data))
                buffer = io.BytesIO()
                tmpFile.save(fp=buffer, format='JPEG')
                pillow_image = ContentFile(buffer.getvalue())
                width, height = tmpFile.size
                name = url.split('/')[-1]
                forma = re.findall(r'\.\S{3}', name)[0]
                if (forma == '.jpg') or (forma == '.png') or (forma == '.bmp'):
                    name = name.split(".")[0] + forma
                    img_obj = Im.objects.create(image_file=InMemoryUploadedFile(pillow_image, None, name, 'image/jpeg', pillow_image.tell,None), widht=width, height=height)
                    return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        images_list = Im.objects.all()
        return render(request, 'list_template.html', {'list': images_list})


class DetailedView(APIView):
    def get(self, request, media_id):
        inst = Im.objects.get(id=media_id)
        data = {"id=": inst.id, "url=": inst.image_url, "picture=": inst.image_file.url, "width=": inst.widht, "height=": inst.height}
        data = json.dumps(data)
        return Response(data)

    def delete(self, request, media_id):
        inst = Im.objects.get(id=media_id)
        inst.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def resize_image(image, width=100, height=100, name=None):
    img = pil_img.open(image)
    new_img = img.resize((width, height))
    buffer = io.BytesIO()
    new_img.save(fp=buffer, format='JPEG')
    return ContentFile(buffer.getvalue())


class ResizerView(APIView):
    def post(self, request, media_id):
        inst = Im.objects.get(id=media_id)
        height = int(request.data.get('height'))
        width = int(request.data.get('width'))
        img_name = inst.image_file.url.split('/')[-1]
        img_path = settings.MEDIA_ROOT + "images" + img_name
        pillow_image = resize_image(inst.image_file, width, height, img_path)
        inst.image_file.save(img_name, InMemoryUploadedFile(pillow_image, None, img_name, 'image/jpeg', pillow_image.tell, None))
        img_obj = Im.objects.filter(id=media_id).update(height=height, widht=width)
        return Response(status=status.HTTP_201_CREATED)



