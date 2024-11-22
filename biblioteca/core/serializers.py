from rest_framework import serializers
from .models import Categoria, Autor, Livro, Colecao


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria
        fields = ('url', 'id', 'nome')


class AutorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Autor
        fields = ('url', 'id', 'nome')


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


class ColecaoSerializer(serializers.HyperlinkedModelSerializer):
    livros = serializers.SlugRelatedField(
        many=True,
        queryset=Livro.objects.all(),
        slug_field='titulo'
    )
    colecionador = serializers.ReadOnlyField(source='colecionador.username')

    class Meta:
        model = Colecao
        fields = ('url', 'id', 'nome', 'descricao', 'colecionador', 'livros')
