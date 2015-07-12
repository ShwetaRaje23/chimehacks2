from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.models import User
from chimehack_server.models import Setting
from django.core.urlresolvers import reverse
import random
from django.contrib import messages
from twilio.rest import TwilioRestClient 

def updateSettingToSession(request, setting):
    request.session['cellphone'] = setting.cellphone
    request.session['emergencyContact'] = setting.emergencyContact
    request.session['SMS'] = setting.SMS
    request.session['MMS'] = setting.MMS
    request.session['redAlertContact'] = setting.redAlertContact
    request.session['secretKey'] = setting.secretKey
    request.session['dailyMessage'] = setting.dailyMessage
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
    if 'MMS' in request.session:
        context.update({'MMS':request.session['MMS']})
    if 'redAlertContact' in request.session:
        context.update({'redAlertContact':request.session['redAlertContact']})
    if 'secretKey' in request.session:
        context.update({'secretKey':request.session['secretKey']})
    if 'dailyMessage' in request.session:
        context.update({'dailyMessage':request.session['dailyMessage']})    
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
    # TODO validate phone number - num of digits
    updateCellphoneToSession(request, cellphone)
    if Setting.objects.filter(cellphone=cellphone):
        updateErrorToSession(request, ["the cellphone has been registered already"])
        return redirect(reverse('home'))

    # TODO usr = cellphone number that should be sent the verification code
    secretKey = "%04d" % random.randint(1, 9999)
    # put your own credentials here 
    ACCOUNT_SID = "AC9434eb9d473cce8c76bc31dd9c16f957" 
    AUTH_TOKEN = "a9d1e7b45ac625670e619b935316257c" 
     
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
     
    client.messages.create(
        to="+" + cellphone, 
        from_="+12132634357", 
        body="Your verification code is " +  secretKey + ". " + " - Meow Cat"
    )

    # verificationCode = secretKey

    # create a new user
    setting = Setting(cellphone = cellphone, secretKey = secretKey, SMS="SMS")
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
        setting = Setting.objects.get(cellphone=cellphone)
        updateSettingToSession(request, setting)
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
    if "MMS" in request.POST:
        setting.MMS = "MMS"
    else:
        setting.MMS = ""
    if "dailyMessage" in request.POST:
        setting.dailyMessage = "dailyMessage"
    else:
        setting.dailyMessage = ""
    setting.redAlertContact = request.POST['redAlertContact']
    setting.secretKey = request.POST['secretKey']
    setting.save()
    updateSettingToSession(request, setting)
    updateSettingFromSession(request, context)
    updateErrorFromSession(request, context)
    context.update({"message": "You've successfully updated your settings! You should receive a text with instructions and your first cat image. Please delete the text if you're uncomfortable with having it on your phone."})
    ACCOUNT_SID = "AC9434eb9d473cce8c76bc31dd9c16f957" 
    AUTH_TOKEN = "a9d1e7b45ac625670e619b935316257c" 
     
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
     
    client.messages.create(
        to="+" + setting.cellphone, 
        from_="+12132634357", 
        body='>>> Meow Cat is here for you! Please respond with: "M" for another image, "T" for terms and conditions (request for help), and "I" anytime you want to see these instructions again. - Meow Cat',
        medxia_url='http://newartcolorz.com/images/2014/1/cute-cat-9281-9771-hd-wallpapers.jpg'
    )
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

def responseToText(request):
    cats = ['http://i.ytimg.com/vi/GchUiYAmlLM/maxresdefault.jpg','http://i.ytimg.com/vi/icqDxNab3Do/maxresdefault.jpg', 'http://wallpaper-download.net/wallpapers/football-wallpapers-funny-cats-smile-wallpaper-31607.jpg']
    
    if request.method == 'GET':
      fromNum = request.GET['From']
      bodyContent = request.GET['Body']
      content = ""
      media_url = ""
      if(bodyContent == 'I'):
        content = 'Meow Cat is here for you! Please respond with: "M" for another image, "T" for terms and conditions (request for help), and "I" anytime you want to see these instructions again. - Meow Cat'
      if(bodyContent == 'T'):
        # send text to local authorities asking for help
        ACCOUNT_SID = "AC9434eb9d473cce8c76bc31dd9c16f957" 
        AUTH_TOKEN = "a9d1e7b45ac625670e619b935316257c" 
     
        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
        setting = Setting.objects.get(cellphone=fromNum)
        url = 'https://chimehacks2-amanicka1.c9.io/contactHelp?who=' + setting.cellphone
        call = client.calls.create(url=url,
          to="+" + setting.redAlertContact,
          from_="+12132634357")
        
        # send text to person asking for help
        content = 'Meow Cat is on the way!'
      if(bodyContent == 'M'):
        content = "Here's your meow cat of the day:"
        media_url = cats[random.randint(0,2)]

      print fromNum
      context = {'fromNum':fromNum, 'content': content, 'media_url': media_url}
      return render(request, 'instructionText.xml', context)

def contactHelp(request):
    context = {}
    print request.GET
    context.update({'who': request.GET['who']})
    return render(request, 'contactHelp.xml', context)

