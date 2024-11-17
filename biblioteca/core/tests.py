from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from core.models import Colecao, Livro, Autor, Categoria
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class ColecaoTests(APITestCase):
    def post_colecao(self, nome, descricao, livros):
        url = reverse("colecao-list")
        data = {
            "nome": nome,
            "descricao": descricao,
            "livros": livros
        }
        response = self.client.post(url, data, format="json")
        return response

    def create_user_and_set_token_credentials(self):
        user = User.objects.create_user(
            username="user01",
            email="user01@example.com",
            password="user01password"
        )
        token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token {0}".format(token.key))
        return user

    def setUp(self):
        self.user = self.create_user_and_set_token_credentials()

        self.autor = Autor.objects.create(nome="Autor Teste")
        self.categoria = Categoria.objects.create(nome="Categoria Teste")
        self.livro1 = Livro.objects.create(
            titulo="Livro de Teste 1",
            autor=self.autor,
            categoria=self.categoria,
            publicado_em="2024-11-16"
        )
        self.livro2 = Livro.objects.create(
            titulo="Livro de Teste 2",
            autor=self.autor,
            categoria=self.categoria,
            publicado_em="2024-11-16"
        )

    def test_post_colecao(self):
        response = self.post_colecao(
            nome="Coleção Teste",
            descricao="Livros de Teste.",
            livros=[self.livro1.titulo, self.livro2.titulo]
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual("user01", Colecao.objects.get().colecionador.username)
