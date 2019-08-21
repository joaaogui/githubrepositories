from django.shortcuts import render
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
scope = 'repo'  # we want to fetch user's email

github = OAuth2Session(client_id, scope=scope)

def index(request):
    authorization_base_url = 'https://github.com/login/oauth/authorize'
    authorization_url, state = github.authorization_url(authorization_base_url)
    return redirect(authorization_url)

def detail(request, repository_id):
    return HttpResponse("You're looking at repository %s." % repository_id)

def repos(request):
    print(request.GET['code'])
    params = {
        'client_id' : client_id,
        'client_secret' :client_secret,
        'code' : request.GET['code']
    }
    header = 'Accept: application/json'
    r = requests.post('https://github.com/login/oauth/access_token', data=params, headers={"Accept": "application/json"})
    result = r.json()
    token = result.get("access_token", None)

    g = Github(token)

    print(g.get_repos())
    for x in g.get_user().get_repos(visibility='all'):
        print(x)
    # get_repos = requests.get('https://api.github.com/user', headers={'Authorization': 'token ' + token})
    # print(get_repos.content)

    # token = github.fetch_token(token_url, username=client_id, password=client_secret, authorization_response=url)
    return HttpResponse("YCHama")

