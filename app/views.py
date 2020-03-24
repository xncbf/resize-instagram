from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        return HttpResponse(status=201)