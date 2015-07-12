from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render, redirect, get_object_or_404


def login(request):
	template = loader.get_template('login.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))
def setup(request):
    context = {}
    return render(request, 'setup.html', context)
def settings(request):
    context = {}
    return render(request, 'settings.html', context)
def register(request):
    context = {}
    return render(request, 'register.html', context)
