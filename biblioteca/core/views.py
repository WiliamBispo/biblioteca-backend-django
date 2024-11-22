from .models import Livro, Autor, Categoria, Colecao
from .serializers import LivroSerializer, AutorSerializer, CategoriaSerializer, ColecaoSerializer
from rest_framework import generics
from core.filters import LivroFilter
from rest_framework import permissions
from core import custom_permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class LivroList(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-list"
    filterset_class = LivroFilter
    search_fields = ("^titulo",)
    ordering_fields = ('titulo', 'autor', 'categoria', 'publicado_em')


class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-detail"


class AutorList(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-list"
    search_fields = ("^nome",)
    ordering_fields = ('nome',)


class AutorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-detail"


class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-list"
    search_fields = ("^nome",)
    ordering_fields = ('nome',)


class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-detail"


class ColecaoList(generics.ListCreateAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    name = "colecao-list"
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(colecionador=self.request.user)


class ColecaoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    name = "colecao-detail"
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsCurrentUserOwnerOrReadOnly
    ]
