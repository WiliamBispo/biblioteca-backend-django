from rest_framework import serializers
from .models import Categoria, Autor, Livro


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    livros = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='livro-detail')

    class Meta:
        model = Categoria
        fields = ('url', 'id', 'nome', 'livros')


class AutorSerializer(serializers.HyperlinkedModelSerializer):
    livros = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='livro-detail')

    class Meta:
        model = Autor
        fields = ('url', 'id', 'nome', 'livros')


class LivroSerializer(serializers.HyperlinkedModelSerializer):
    autor = serializers.SlugRelatedField(
        queryset=Autor.objects.all(), slug_field='nome'
    )
    categoria = serializers.SlugRelatedField(
        queryset=Categoria.objects.all(), slug_field='nome'
    )

    class Meta:
        model = Livro
        fields = ('url', 'id', 'titulo', 'autor', 'categoria', 'publicado_em')
