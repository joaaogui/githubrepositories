from django.urls import path

from . import views


app_name = 'repositories'

urlpatterns = [
    path('', views.home, name='home'),
    path('add_tag/<int:repository_id>', views.add_tag, name='add_tag'),
    path('<int:repository_id>/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
]