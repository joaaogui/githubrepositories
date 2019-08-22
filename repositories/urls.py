from django.urls import path

from . import views

app_name = 'repositories'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:repository_id>/', views.detail, name='detail'),
    path('button/', views.button, name='button'),
    path('callback/', views.repos),
    path('repositories/', views.repos),
]