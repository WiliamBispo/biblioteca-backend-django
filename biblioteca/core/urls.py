from django.urls import path
from . import views


urlpatterns = [

    path('livros/', views.LivroList.as_view(), name=views.LivroList.name),
    path('livros/<int:pk>/', views.LivroDetail.as_view(),
         name=views.LivroDetail.name),

    path('categoria/', views.CategoriaList.as_view(),
         name=views.CategoriaList.name),
    path('categoria/<int:pk>/', views.CategoriaDetail.as_view(),
         name=views.CategoriaDetail.name),

    path('autor/', views.AutorList.as_view(), name=views.AutorList.name),
    path('autor/<int:pk>/', views.AutorDetail.as_view(),
         name=views.AutorDetail.name),

    path('colecoes/', views.ColecaoList.as_view(), name=views.ColecaoList.name),
    path('colecoes/<int:pk>/', views.ColecaoDetail.as_view(),
         name=views.ColecaoDetail.name),

]
