from allauth.socialaccount.models import SocialToken
from django.shortcuts import render, redirect
from django.views.generic import ListView
from github import Github
from .models import Repository


def home(request):
    if request.user.is_authenticated:
        access_token = SocialToken.objects.get(account__user=request.user,
                                               account__provider='github')
        repository_list = []
        g = Github(str(access_token))
        db_repos = list(Repository.objects.all().values_list('id', flat=True))

        for repo in g.get_user().get_repos():
            repository_list.append(repo)
            print(type(repo.id))
            print(type(db_repos))
            if repo.id in db_repos:
                print(type(repo))
        return (render(request, 'repositories/index.html', {"repository_list": repository_list}))
    else:
        return (render(request, 'repositories/index.html'))


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


def add_tag(request, repository_id):
    if request.method == "POST":
        print(request.POST.get('tag'))
        repo, exists = Repository.objects.get_or_create(id=repository_id)
        repo.tags.add(request.POST.get('tag'))
        repo.save()
    return redirect('/')