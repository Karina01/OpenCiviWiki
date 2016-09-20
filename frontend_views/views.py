import json

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from api.models import Category, Account, Topic, Civi

from legislation import sunlightapi as sun
from utils.custom_decorators import beta_blocker, login_required

def base_view(request):
    if not request.user.is_authenticated():
        return TemplateResponse(request, 'static_templates/landing.html', {})

    a = Account.objects.get(user=request.user)
    if not a.beta_access:
        return HttpResponseRedirect('/beta')
    return TemplateResponse(request, 'feed.html', {})



@login_required
@beta_blocker
def user_profile(request, username=None):
    if not username:
        return HttpResponseRedirect('/profile/{0}'.format(request.user))

    else:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponseRedirect('/404')

    return TemplateResponse(request, 'account.html', {'username': user})


@login_required
@beta_blocker
def issue_thread(request, thread_id=None):
    if not thread_id:
        return HttpResponseRedirect('/404')

    # t = Thread.objects.get(id=thread_id)

    return TemplateResponse(request, 'thread.html', {'thread_id': thread_id})

@login_required
@beta_blocker
def create_group(request):
    return TemplateResponse(request, 'newgroup.html', {})

@login_required
@beta_blocker
def dbview(request):
    result = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]

    return TemplateResponse(request, 'dbview.html', {'result': json.dumps(result)})

@login_required
@beta_blocker
def add_civi(request):
    categories = [{'id': c.id, 'name': c.name} for c in Category.objects.all()]
    topics = [{'id': c.id, 'topic': c.topic} for c in Topic.objects.all()]

    return TemplateResponse(request, 'add_civi.html', {'categories': json.dumps(categories), 'topics': json.dumps(topics)})

def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    return TemplateResponse(request, 'login.html', {})

def beta_view(request):
    return TemplateResponse(request, 'beta_blocker.html', {})

def declaration(request):
    return TemplateResponse(request, 'declaration.html', {})

def landing_view(request):
    return TemplateResponse(request, 'static_templates/landing.html', {})

def how_it_works_view(request):
    return TemplateResponse(request, 'static_templates/how_it_works.html', {})

def about_view(request):
    return TemplateResponse(request, 'static_templates/about.html', {})

def support_us_view(request):
    return TemplateResponse(request, 'static_templates/support_us.html', {})

def does_not_exist(request):
    return TemplateResponse(request, 'base/404.html', {})
