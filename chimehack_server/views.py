from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render, redirect, get_object_or_404


def login(request):
	template = loader.get_template('login.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))
def signup(request):
    context = {'usr':request.GET['usr']}
    return render(request, 'signup.html', context)
def settings(request):
    context = {}
    return render(request, 'settings.html', context)
def home(request):
    context = {}
    return render(request, 'home.html', context)
# default response to a text
# look at the content of the message and decide what to do
def dresponseToText(request):
    if request.method == 'GET':
      print "before from"
      fromNum = request.GET['From']
      print fromNum
      context = {'fromNum':fromNum}
      return render(request, 'dresponseToText.xml', context)
