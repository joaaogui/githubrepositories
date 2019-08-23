from allauth.socialaccount.models import SocialToken
import requests
from django.shortcuts import render
from django.shortcuts import redirect
from github import Github
from django.views.generic import ListView
from .models import Repository, Tag

from django.views.generic import TemplateView


def home(request):

    if request.user.is_authenticated:
        access_token = SocialToken.objects.get(account__user=request.user,
                                               account__provider='github')
        repository_list = []
        g = Github(str(access_token))
        for repo in g.get_user().get_repos():
            repository_list.append(repo)
        return(render(request, 'repositories/index.html', {"repository_list": repository_list} ))
    else:
        return(render(request, 'repositories/index.html'))


def detail(request, repository_id):
    access_token = SocialToken.objects.get(account__user=request.user,
                                               account__provider='github')
    g = Github(str(access_token))
    repo = g.get_repo(repository_id)

    # TODO: get tags to show in detail
    # tags = Repository.objects.filter(tag__name__icontains=query)
    context = {
        'id': repo.id,
        'name': repo.name,
        'description': repo.description,
        'created_at': repo.created_at
    }

    request.session['repository_id'] = repo.id
    return render(request, 'repositories/detail.html', {'context': context})


def create_tag(request):
    id = request.session['repository_id']
    print(id)
    print(request.POST['tag'])
    repository, created = Repository.objects.get_or_create(id=id)
    repository.save()
    tag, created = Tag.objects.get_or_create(name=request.POST['tag'])
    tag.save()

    repository.tag.add(tag)
    return redirect('/' + str(id))


class SearchResultsView(ListView):
    model = Tag
    template_name = 'repositories/search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        return Repository.objects.filter(tag__name__icontains=query)
