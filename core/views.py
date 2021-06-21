from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q

from api.models import Outfit
from .forms import ChangeUserInfoForm, RegisterUserFrom, BbForm, AIFormSet, OutfitForm
from .models import AdvUser, Bb, SubCategory
# Create your views here.

def index(request):
    bbs = Bb.objects.filter(is_active=True)[:10]
    context = {'bbs': bbs}
    return render(request, 'main/index.html', context)


def about(request):
    return render(request, 'main/about.html')


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404

    return HttpResponse(template.render(request=request))


def detail(request, category_pk, pk):
    bb = get_object_or_404(Bb, pk=pk)
    user_id = request.user.pk
    context = {'bb': bb, 'user_id': user_id}
    return render(request, 'main/detail.html', context)


def by_category(request, pk):
    category = get_object_or_404(SubCategory, pk=pk)
    bbs = Bb.objects.filter(is_active=True, category=pk)
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'category': category, 'page': page, 'bbs': page.object_list}

    return render(request, 'main/by_rubric.html', context)


@login_required
def profile(request):
    bbs = Bb.objects.filter(author=request.user.pk)
    outfits = Outfit.objects.filter(author=request.user.pk)
    context = {'bbs': bbs, 'outfits': outfits}
    return render(request, 'main/profile.html', context)


@login_required
def profile_bb_detail(request, pk, *args):
    bb = get_object_or_404(Bb, pk=pk)
    ais = '' # bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'main/profile_bb_detail.html', context)


@login_required
def profile_bb_add(request):
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Объявление добавлено')
                return redirect('core:profile')
    else:
        form = BbForm(initial={'author': request.user.pk})
        formset = AIFormSet()
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_bb_add.html', context)


def profile_bb_change(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES, instance=bb)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Объявление исправлено')
                return redirect('core:profile')
    else:
        form = BbForm(instance=bb)
        formset = AIFormSet(instance=bb)
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_bb_change.html', context)


@login_required
def profile_bb_delete(request, pk):
    bb = get_object_or_404(Bb, pk=pk)
    if request.method == 'POST':
        bb.delete()
        messages.add_message(request, messages.SUCCESS, 'Объявление удалено')
        return redirect('core:profile')
    else:
        context = {'bb': bb}
        return render(request, 'main/profile_bb_delete.html', context)


@login_required
def profile_outfit_add(request):
    if request.method == 'GET':
        form = OutfitForm(initial={'author': request.user.pk})
    else:
        form = OutfitForm(request.POST, request.FILES)
        if form.is_valid():
            outf = form.save()
            messages.add_message(request, messages.SUCCESS, 'Образ добавлен')
            return redirect('core:profile')
    context = {'form': form}
    return render(request, 'main/profile_outfit_add.html', context)

@login_required
def profile_outfit_change(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk)
    if request.method == 'GET':
        form = OutfitForm(instance=outfit)
    else:
        form = OutfitForm(request.POST, request.FILES, instance=outfit)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Образ изменён')
                return redirect('core:profile')
    context = {'form': form}
    return render(request, 'main/profile_outfit_change.html', context)


@login_required
def profile_outfit_delete(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk)
    if request.method == 'GET':
        return render(request, 'main/profile_outfit_delete.html', context={'outfit': outfit})
    else:
        outfit.delete()
        messages.add_message(request, messages.SUCCESS, 'Образ удалён')
        return redirect('core:profile')


class TSLoginView(LoginView):
    template_name = 'main/login.html'


class TSLogoutView(LogoutView):
    template_name = 'main/logout.html'


# LoginRequiredMixin допускает к странице только авторизованных пользователей
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('core:profile')
    success_message = 'Данные пользователя изменены'

    # Извлекаем ключ пользователя и сохраняем его в атрибуте user_id
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    # Извлекаем исправляемую запись
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserFrom
    success_url = reverse_lazy('core:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('core:index')

    # Сохранили ключ текущего пользователя
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)

    # Нашли удаляемого пользователя
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
