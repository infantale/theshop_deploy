from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from .forms import ChangeUserInfoForm
from .models import AdvUser
# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404

    return HttpResponse(template.render(request=request))

@login_required
def profile(request):
    return render(request, 'main/profile.html')


class TSLoginView(LoginView):
    template_name = 'main/login.html'


class TSLogoutView(LogoutView):
    template_name = 'main/logout.html'


# class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, LogUpdateView):
#     model = AdvUser
#     template_name = 'main/change_user_info.html'
#     form_class = ChangeUserInfoForm
#     success_url = reverse_lazy('core:profile')
#     success_message = 'Данные пользователя изменены'
    # 610
