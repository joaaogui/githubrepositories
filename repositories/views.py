from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import requests
from authlib.client import OAuth2Session
# from requests_oauthlib import OAuth2Session
import oauthlib
from django.shortcuts import redirect
from github import Github
import json
from authlib.django.client import OAuth

from django.views.generic import TemplateView, ListView


from django.template import loader

from .models import Repository, OAuth2Token, Tag

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

# oauth.github.get('user')

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
    OAuth2Token.objects.get_or_create(name='github', user=request.user, access_token=token.get("access_token", None))
    token = token.get("access_token", None)
    repository_list = []
    g = Github(token)
    for x in g.get_user().get_repos(visibility='all'):
        repository_list.append(x)


    return render(request, 'repositories/index.html', {'repository_list': repository_list})

def fetch_token(request):
    item = OAuth2Token.objects.filter(
        name='github',
        user=request.user
    )
    return item.last().to_token()

def button(request):
    authorization_base_url = 'https://github.com/login/oauth/authorize'
    authorization_url, state = github.authorization_url(authorization_base_url)
    return redirect(authorization_url)

def detail(request, repository_id):
    # repository = get_object_or_404(Repository, pk=repository_id)
    # print(dir(request))
    # print(request.user)
    token = fetch_token(request)
    g = Github(token.get("access_token", None))
    repo = g.get_repo(repository_id)
    context = {
        'id': repo.id,
        'name' : repo.name,
        'description': repo.description,
        'created_at': repo.created_at
    }
    # print
    request.session['repository_id'] = repo.id
    return render(request, 'repositories/detail.html', {'context': context})

# def get_info(token, repository_id):
#

def repos(request):
    params = {
        'client_id' : client_id,
        'client_secret' :client_secret,
        'code' : request.GET['code']
    }
    r = requests.post('https://github.com/login/oauth/access_token', data=params, headers={"Accept": "application/json"})
    result = r.json()
    token = result.get("access_token", None)

    g = Github(token)

    repository_list = []
    # print(g.get_repo('202746182'))
    for x in g.get_user().get_repos(visibility='all'):
        repository_list.append(x)


    return render(request, 'repositories/index.html', {'repository_list': repository_list})


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