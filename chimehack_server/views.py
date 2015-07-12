from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.models import User
from chimehack_server.models import Setting
from django.core.urlresolvers import reverse
import random
from django.contrib import messages
def updateSettingToSession(request, setting):
    request.session['cellphone'] = setting.cellphone
    request.session['emergencyContact'] = setting.emergencyContact
    request.session['SMS'] = setting.SMS
    request.session['call'] = setting.call
    request.session['redAlertContact'] = setting.redAlertContact
    request.session['secretKey'] = setting.secretKey
def updateErrorToSession(request, errors):
    request.session['errors'] = errors
def updateCellphoneToSession(request, cellphone):
    request.session['cellphone'] = cellphone
def updateSecretKeyToSession(request, secretKey):
    request.session['secretKey'] = secretKey
def updateSettingFromSession(request, context):
    if 'cellphone' in request.session:
        context.update({'cellphone':request.session['cellphone']})
    if 'emergencyContact' in request.session:
        context.update({'emergencyContact':request.session['emergencyContact']})
    if 'SMS' in request.session:
        context.update({'SMS':request.session['SMS']})
    if 'call' in request.session:
        context.update({'call':request.session['call']})
    if 'redAlertContact' in request.session:
        context.update({'redAlertContact':request.session['redAlertContact']})
    if 'secretKey' in request.session:
        context.update({'secretKey':request.session['secretKey']})
def updateCellphoneFromSession(request, context):
    if 'cellphone' in request.session:
        context.update({'cellphone':request.session['cellphone']})

def updateErrorFromSession(request, context):
    if 'errors' in request.session and request.session['errors']:
        context.update({'errors':request.session['errors']})
        request.session['errors'] = []

def home(request):
    # GET only
    context = {}
    updateCellphoneFromSession(request, context)
    updateErrorFromSession(request, context)
    return render(request, 'home.html', context)
def signup(request):
    context = {}
    if request.method == 'GET':
        updateCellphoneFromSession(request, context)
        updateErrorFromSession(request, context)
        return render(request, 'signup.html', context)
    if request.method != 'POST':
        updateErrorToSession(request, ["unsupported request"])
        return redirect(reverse('signup'))
    if not 'cellphone' in request.POST:
        updateErrorToSession(request, ["no cellphone is found"])
        return redirect(reverse(home))
    cellphone = request.POST['cellphone']
    updateCellphoneToSession(request, cellphone)
    if Setting.objects.filter(cellphone=cellphone):
        updateErrorToSession(request, ["the cellphone has been registered already"])
        return redirect(reverse('home'))

    # TODO usr = cellphone number that should be sent the verification code
    secretKey = "1234" # "%04d" % random.randint(1, 9999)
    # verificationCode = secretKey

    # create a new user
    setting = Setting(cellphone = cellphone, secretKey = secretKey)
    setting.save()
    updateCellphoneFromSession(request, context)
    updateErrorFromSession(request, context)
    return render(request, 'signup.html', context)
def verification(request):
    context = {}
    if request.method != 'POST':
        updateErrorToSession(request, ["MUST be POST"])
        return redirect(reverse('home'))
    if not 'cellphone' in request.POST or not 'secretKey' in request.POST:
        updateErrorToSession(request, ["cellphone or secretKey is not found"])
        return redirect(reverse('home'))
    cellphone = request.POST['cellphone']
    updateCellphoneToSession(request, cellphone)
    secretKey = request.POST['secretKey']
    updateSecretKeyToSession(request, secretKey)
    if not Setting.objects.filter(cellphone=cellphone, secretKey=secretKey):
        updateErrorToSession(request, ["the code is incorrect"])
        return redirect(reverse('signup'))
    return redirect(reverse('settings'))
def login(request):
    context = {}
    if request.method == 'GET':
        updateCellphoneFromSession(request, context)
        updateErrorFromSession(request, context)
        return render(request, 'login.html', context)
    if request.method != 'POST':
        updateErrorToSession(request, ["unknown request"])
        return redirect(reverse('home'))
    if not 'cellphone' in request.POST or not 'secretKey' in request.POST:
        updateErrorToSession(request, ["cellphone or secretKey is not found"])
        return redirect(reverse('home'))
    cellphone = request.POST['cellphone']
    updateCellphoneToSession(request, cellphone)
    secretKey = request.POST['secretKey']
    updateSecretKeyToSession(request, secretKey)
    if not Setting.objects.filter(cellphone=cellphone, secretKey=secretKey):
        updateErrorToSession(request, ["the cellphone and secretKey is not matched"])
        return redirect(reverse('login'))
    return redirect(reverse('settings'))
def settings(request):
    context = {}
    if request.method == 'GET':
        if not 'cellphone' in request.session:
            updateErrorToSession(request, ["no cellphone is found"])
            return redirect(reverse('home'))
        if not 'secretKey' in request.session:
            updateErrorToSession(request, ["no secretKey is found"])
            return redirect(reverse('home'))
        cellphone = request.session['cellphone']
        secretKey = request.session['secretKey']
        if not Setting.objects.filter(cellphone=cellphone, secretKey=secretKey):
            updateErrorToSession(request, ["the secretKey is incorrect"])
            return redirect(reverse('home'))
        updateSettingFromSession(request, context)
        updateErrorFromSession(request, context)
        return render(request, 'settings.html', context)
    if request.method != 'POST':
        updateErrorToSession(request, ["unknown request"])
        return redirect(reverse('home'))
    print request.POST
    if not 'cellphone' in request.POST or not 'secretKey' in request.POST:
        updateErrorToSession(request, ["no cellphone or secretKey is found"])
        return redirect(reverse('home'))
    cellphone = request.POST['cellphone']
    if not Setting.objects.filter(cellphone=cellphone):
        updateErrorToSession(request, ["cellphone not found"])
        return redirect(reverse('home'))
    setting = Setting.objects.get(cellphone=cellphone)
    setting.cellphone = request.POST['cellphone']
    setting.emergencyContact = request.POST['emergencyContact']
    if "SMS" in request.POST:
        setting.SMS = "SMS"
    else:
        setting.SMS = ""
    if "call" in request.POST:
        setting.call = "call"
    else:
        setting.call = ""
    setting.redAlertContact = request.POST['redAlertContact']
    setting.secretKey = request.POST['secretKey']
    setting.save()
    updateSettingToSession(request, setting)
    updateSettingFromSession(request, context)
    updateErrorFromSession(request, context)
    return render(request, 'settings.html', context)

# default response to a text
# look at the content of the message and decide what to do
def dresponseToText(request):
    if request.method == 'GET':
      print "before from"
      fromNum = request.GET['From']
      print fromNum
      context = {'fromNum':fromNum}
      return render(request, 'dresponseToText.xml', context)
