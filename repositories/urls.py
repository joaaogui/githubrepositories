from django.urls import path

from . import views
from .views import  SearchResultsView


app_name = 'repositories'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:repository_id>/', views.detail, name='detail'),
    path('login/', views.login, name='login'),
    path('create_tag/', views.create_tag, name='create_tag'),
    path('callback/', views.authorize),
    path('repositories/', views.repos),
    path('search_results/', SearchResultsView.as_view(), name='search_results'),
]