from django.urls import path

from . import views


app_name = 'repositories'

urlpatterns = [
    path('', views.home, name='home'),
    path('add_tag/<int:repository_id>/<str:repository_name>', views.add_tag, name='add_tag'),
    path('<int:repository_id>/', views.repository_detail, name='repository_detail'),
    path('search/', views.search, name='search'),
    path('tags/', views.tag_list, name='tag_list'),
    path('remove_tag/<str:tag_slug>', views.remove_tag, name="remove_tag"),
    path('remove_tag_repository/<int:repository_id>/<str:tag_name>', views.remove_tag_repository, name="remove_tag_repository")

]