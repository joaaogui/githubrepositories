from django.shortcuts import render
from authlib.client import OAuth2Session
from authlib.django.client import OAuth
from django.shortcuts import redirect
from github import Github
from django.views.generic import ListView
from .models import Repository, Tag

oauth = OAuth()

oauth.register(
    name='github',
    client_id='181ce723b9ce46e40263',
    client_secret="f9e0cc40dc6f080c9752a0f79f258683601422a5",
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'repo'},
)

client_id = "181ce723b9ce46e40263"
token_url = 'https://github.com/login/oauth/access_token'
client_secret = "f9e0cc40dc6f080c9752a0f79f258683601422a5"
scope = 'repo'

github = OAuth2Session(client_id, scope=scope)


def index(request):
    return render(request, 'repositories/index.html')


def login(request):
    # build a full authorize callback uri
    redirect_uri = request.build_absolute_uri('/callback')
    return oauth.github.authorize_redirect(request, redirect_uri)


def authorize(request):
    token = oauth.github.authorize_access_token(request)
    # resp = oauth.github.get('user')
    token = token.get("access_token", None)
    request.session["token"] = token
    repository_list = []
    g = Github(token)
    for x in g.get_user().get_repos(visibility='all'):
        repository_list.append(x)

    return render(request, 'repositories/index.html', {'repository_list': repository_list})


def detail(request, repository_id):
    token = request.session['token']
    g = Github(token)
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
