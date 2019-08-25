from allauth.socialaccount.models import SocialToken
from django.shortcuts import render, redirect
from github import Github
from .models import Repository
from taggit.models import Tag


def home(request):
    if request.user.is_authenticated:
        access_token = SocialToken.objects.get(account__user=request.user,
                                               account__provider='github')
        repository_list = []
        g = Github(str(access_token))
        db_repos = list(Repository.objects.all().values_list('id', flat=True))

        for repo in g.get_user().get_repos():
            if str(repo.id) in db_repos:
                repoX = Repository.objects.get(id=repo.id)
                repo.tags = list(repoX.tags.names())
            repository_list.append(repo)
        return (render(request, 'repositories/index.html', {"repository_list": repository_list}))
    else:
        return (render(request, 'repositories/welcome.html'))


def detail(request, repository_id):
    access_token = SocialToken.objects.get(account__user=request.user,
                                           account__provider='github')
    print(access_token)
    g = Github(str(access_token))

    repo = g.get_repo(repository_id)

    if len(Repository.objects.filter(id=repository_id)):
        db_repo = Repository.objects.get(id=repository_id)
        tags = db_repo.tags.names()
    else:
        tags = ""

    # TODO: get tags to show in detail
    # if Repository.objects.get(id=repository_id) :
    repository = {
        'id': repo.id,
        'name': repo.name,
        'description': repo.description,
        'tags': list(tags)
    }

    return render(request, 'repositories/detail.html', {'repository': repository})


def add_tag(request, repository_id, repository_name):
    repo, exists = Repository.objects.get_or_create(id=repository_id, name=repository_name)
    print(repo)
    repo.tags.add(request.POST.get('tag'))
    repo.save()
    return redirect('/')


def remove_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    tag.delete()
    return redirect('/tags/')


def remove_tag_repository(request, tag_name, repository_id):
    repo, exists = Repository.objects.get_or_create(id=repository_id)
    repo.tags.remove(tag_name)
    return redirect('/' + str(repository_id))


def tags(request):
    tag_list = Tag.objects.all()
    return render(request, 'repositories/tags.html', {'tag_list': tag_list})


def search(request):
    input = request.GET.get('tag')
    repos = Repository.objects.filter(tags__name__in=[input])
    repository_list = []
    for repo in repos:
        repo.tags = list(repo.tags.names())
        repository_list.append(repo)
    return render(request, 'repositories/index.html', {"repository_list": repository_list})
