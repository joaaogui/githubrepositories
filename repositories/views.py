from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Repository


def index(request):
    latest_repository_list = Repository.objects.order_by('-search_date')[:20]
    template = loader.get_template('repositories/index.html')
    context = {'latest_repository_list': latest_repository_list}
    return render(request, 'repositories/index.html', context)


def detail(request, repository_id):
    return HttpResponse("You're looking at repository %s." % repository_id)
