from django.http import HttpResponse
from django.template import RequestContext, loader


def login(request):
	template = loader.get_template('login.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))
