from django.urls import path

from . import views
from .views import  SearchResultsView


app_name = 'repositories'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:repository_id>/', views.detail, name='detail'),
    path('create_tag/', views.create_tag, name='create_tag'),
    path('search_results/', SearchResultsView.as_view(), name='search_results'),
]