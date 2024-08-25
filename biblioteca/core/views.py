from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Livro
from .serializers import LivroSerializer


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def livro_list_create(request):
    if request.method == 'GET':
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        livro_data = JSONParser().parse(request)
        serializer = LivroSerializer(data=livro_data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def livro_detail(request, pk):
    try:
        livro = Livro.objects.get(pk=pk)
    except Livro.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LivroSerializer(livro)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        livro_data = JSONParser().parse(request)
        serializer = LivroSerializer(livro, data=livro_data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        livro.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
