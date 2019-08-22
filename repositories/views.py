from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import requests
from requests_oauthlib import OAuth2Session
from django.shortcuts import redirect
from github import Github
import json

from django.template import loader

from .models import Repository


client_id = "181ce723b9ce46e40263"
token_url = 'https://github.com/login/oauth/access_token'
client_secret = "f9e0cc40dc6f080c9752a0f79f258683601422a5"
scope = 'repo'

github = OAuth2Session(client_id, scope=scope)

def index(request):
    return render(request, 'repositories/index.html')

def button(request):
    print('chama')
    authorization_base_url = 'https://github.com/login/oauth/authorize'
    authorization_url, state = github.authorization_url(authorization_base_url)
    return redirect(authorization_url)

def detail(request, repository_id):
    # repository = get_object_or_404(Repository, pk=repository_id)

    return render(request, 'repositories/detail.html', {'repository': repository_id})

# def get_info(token, repository_id):
#

def repos(request):
    print(request.GET['code'])
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
        print(x.id)
        print(" ---------------------------------------- --------------------------------")


    return render(request, 'repositories/index.html', {'repository_list': repository_list})

