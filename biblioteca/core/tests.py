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

    # Criação e associação do token ao primeiro usuario.
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

    # Criação e associação do token ao segundo usuario.
    def create_second_user_and_set_token_credentials(self):
        user_02 = User.objects.create_user(
            username="user02",
            email="user02@example.com",
            password="user02password"
        )
        token = Token.objects.create(user=user_02)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token {0}".format(token.key))
        return user_02

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

    # Teste de Criação de uma nova coleção e associação correta do usuario autenticado
    def test_post_colecao(self):
        response = self.post_colecao(
            nome="Coleção Teste",
            descricao="Livros de Teste.",
            livros=[self.livro1.titulo, self.livro2.titulo]
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        colecao_id = response.data["id"]
        colecao = Colecao.objects.get(id=colecao_id)
        self.assertEqual(self.user, colecao.colecionador)

    # teste do colecionador que pode editar a sua coleção
    def test_put_colecao(self):
        response = self.post_colecao(
            nome="Coleção Teste",
            descricao="Livros de Teste.",
            livros=[self.livro1.titulo, self.livro2.titulo]
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        colecao_id = response.data["id"]

        url = reverse("colecao-detail", args=[colecao_id])
        updated_data = {
            "nome": "Coleção Atualizada",
            "descricao": "Descrição Atualizada.",
            "livros": [self.livro1.titulo]
        }
        put_response = self.client.put(url, updated_data, format="json")
        self.assertEqual(status.HTTP_200_OK, put_response.status_code)
        self.assertEqual("Coleção Atualizada",
                         Colecao.objects.get(id=colecao_id).nome)

    # teste do colecionador que pode excluir a sua coleção
    def test_delete_colecao(self):
        response = self.post_colecao(
            nome="Coleção Teste",
            descricao="Livros de Teste.",
            livros=[self.livro1.titulo, self.livro2.titulo]
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        colecao_id = response.data["id"]

        url = reverse("colecao-detail", args=[colecao_id])
        delete_response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT,
                         delete_response.status_code)
        self.assertFalse(Colecao.objects.filter(id=colecao_id).exists())

    # teste do colecionador que NÃO pode editar ou excluir a coleção de outro colecionador
    def test_put_and_delete_non_colecionador(self):
        response = self.post_colecao(
            nome="Coleção Teste",
            descricao="Livros de Teste.",
            livros=[self.livro1.titulo, self.livro2.titulo]
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        colecao_id = response.data["id"]

        self.create_second_user_and_set_token_credentials()

        url = reverse("colecao-detail", args=[colecao_id])
        updated_data = {
            "nome": "Tentativa de Atualização",
            "descricao": "Tentativa de atualização da Coleção.",
            "livros": [self.livro1.titulo]
        }
        put_response = self.client.put(url, updated_data, format="json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, put_response.status_code)

        delete_response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         delete_response.status_code)

    # teste de usuarios não autenticados que não podem criar coleções
    def test_post_colecao_without_token(self):
        self.client.credentials()
        response = self.post_colecao(
            nome="Coleção Teste",
            descricao="Livros de Teste.",
            livros=[self.livro1.titulo, self.livro2.titulo]
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    # teste de usuarios não autenticados que não podem editar coleções
    def test_put_colecao_without_token(self):
        response = self.post_colecao(
            nome="Coleção Teste",
            descricao="Livros de Teste.",
            livros=[self.livro1.titulo, self.livro2.titulo]
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        colecao_id = response.data["id"]

        self.client.credentials()

        url = reverse("colecao-detail", args=[colecao_id])
        updated_data = {
            "nome": "Tentativa de Atualização",
            "descricao": "Tentativa de atualização da Coleção.",
            "livros": [self.livro1.titulo]
        }
        put_response = self.client.put(url, updated_data, format="json")
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,
                         put_response.status_code)

    # teste de usuarios não autenticados que não podem excluir coleções
    def test_delete_colecao_without_token(self):
        response = self.post_colecao(
            nome="Coleção Teste",
            descricao="Livros de Teste.",
            livros=[self.livro1.titulo, self.livro2.titulo]
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        colecao_id = response.data["id"]

        self.client.credentials()

        url = reverse("colecao-detail", args=[colecao_id])
        delete_response = self.client.delete(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,
                         delete_response.status_code)
