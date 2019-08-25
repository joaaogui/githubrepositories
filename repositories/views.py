from django.shortcuts import render, redirect
from github import Github

from repositories.utils import get_token
from .models import Repository
from taggit.models import Tag


# View function that controls the index page
def home(request):

    # Checks if user is already logged in, if not, redirects to welcome page.
    if request.user.is_authenticated:
        # Gets the token from the allauth saved models, check https://django-allauth.readthedocs.io/en/latest/
        access_token = get_token(request)
        repository_list = []
        github_instance = Github(str(access_token))

        # Return a list with the id's of all repos that had a tag added to it
        repositories_with_tags = list(Repository.objects.all().values_list('id', flat=True))

        # Iterate through the whole list of user repositories for a match with the repositories with tags in the db
        for repository in github_instance.get_user().get_repos():
            # If the repo has already tags added, the tags are saved in it a list, to return ir to the template
            if str(repository.id) in repositories_with_tags:
                repository_with_tag = Repository.objects.get(id=repository.id)
                repository.tags = list(repository_with_tag.tags.names())
            repository_list.append(repository)
        return (render(request, 'repositories/index.html', {"repository_list": repository_list}))
    else:
        return (render(request, 'repositories/welcome.html'))


# View function that controls the repository in detail visualization
def repository_detail(request, repository_id):

    # Gets the token from the allauth saved models, check https://django-allauth.readthedocs.io/en/latest/
    access_token = get_token(request)
    github_instance = Github(str(access_token))

    # if the requested repository already has tags, they are saved as a list for the template,
    if len(Repository.objects.filter(id=repository_id)):
        db_repo = Repository.objects.get(id=repository_id)
        tags = db_repo.tags.names()
    # If the repository has no tags, a empyt string is returned.
    else:
        tags = ""

    # Finds the repo on the API to show additional information
    repository = github_instance.get_repo(repository_id)
    repository_info = {
        'id': repository.id,
        'name': repository.name,
        'description': repository.description,
        'tags': list(tags)
    }

    return render(request, 'repositories/detail.html', {'repository': repository_info})


# View function that controls the addition of tags to the database
def add_tag(request, repository_id, repository_name):
    repo, exists = Repository.objects.get_or_create(id=repository_id, name=repository_name)
    repo.tags.add(request.POST.get('tag'))
    repo.save()
    return redirect('/')

# View function that controls the removal of tags of the database
def remove_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    tag.delete()
    return redirect('/tags/')

# View function that controls the removal of rlation between a Tag and a Repository
def remove_tag_repository(request, tag_name, repository_id):
    repo, exists = Repository.objects.get_or_create(id=repository_id)
    repo.tags.remove(tag_name)
    return redirect('/' + str(repository_id))

# View function that controls the list showing of all tags
def tag_list(request):
    tag_list = Tag.objects.all()
    return render(request, 'repositories/tags.html', {'tag_list': tag_list})

# View function that controls the search of tags in the index visualization
def search(request):
    input = request.GET.get('tag')
    matching_repositories = Repository.objects.filter(tags__name__in=[input])
    repository_list = []
    for repository in matching_repositories:
        repository.tags = list(repository.tags.names())
        repository_list.append(repository)
    return render(request, 'repositories/index.html', {"repository_list": repository_list})
