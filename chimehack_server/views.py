from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.models import User
from chimehack_server.models import Setting

def signup(request):
    # linked from home
    print request.POST
    if not 'cellphone' in request.POST:
        context = {'error' : 'phone can not be empty'}
        print "no cellphone is provided"
        return render(request, 'home.html', context)
    cellphone = request.POST['cellphone']
    setting = Setting(cellphone = cellphone)
    setting.save()
    # TODO usr = cellphone number that should be sent the verification code
    token = "1234"
    context = {'cellphone':cellphone}
    return render(request, 'signup.html', context)
def settings(request):
    context = {}
    return render(request, 'settings.html', context)
def home(request):
    context = {}
    return render(request, 'home.html', context)
@transaction.atomic
def register(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'register.html', context)
    print request.POST['password1']
    new_user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password1'])
    new_user.save()
    # TODO send random verification code cellphone number
    context.update({'usr':request.POST['username']})
    return render(request, 'signup.html', context)

# default response to a text
# look at the content of the message and decide what to do
def dresponseToText(request):
    if request.method == 'GET':
      print "before from"
      fromNum = request.GET['From']
      print fromNum
      context = {'fromNum':fromNum}
      return render(request, 'dresponseToText.xml', context)
