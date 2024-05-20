import random
import pytz
from django.utils import timezone
from pathlib import Path
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, DeleteView

from .filters import ReplyFilter
from .forms import *

from .models import *


def code_gen():
    confirm_code = "".join([random.choice('0123456789') for i in range(6)])
    return confirm_code


####################################### классы представлений ######################################################
class PostList(ListView):
    ordering = '-time_in'
    model = Post
    template_name = 'boardapp/main.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['try_user'] = user
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


class PostDetail(DetailView):
    model = Post
    template_name = 'boardapp/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rep_list = PostReply.objects.filter(announce=self.object).order_by('-time_in')
        context['replist'] = rep_list
        return context


class PostReplyView(LoginRequiredMixin, ListView):
    model = PostReply
    ordering = '-time_in'
    template_name = 'boardapp/profile.html'
    context_object_name = 'replies'

    def get_filter(self):
        return ReplyFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs.filter(announce__author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.get_filter()
        context['posts'] = Post.objects.filter(author=self.request.user)
        return context


#редактирование объявления
class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = AddForm
    template_name = 'boardapp/add.html'

    def get_object(self, queryset=None):
        obj = super(PostEdit, self).get_object()
        if obj.author != self.request.user:
            return Http404
        else:
            return obj

    def get_success_url(self):
        return reverse('main')


#удаление объявления
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'boardapp/delete.html'
    success_url = reverse_lazy('main')

    def get_object(self, queryset=None):
        obj = super(PostDelete, self).get_object()
        if obj.author != self.request.user:
            return Http404
        else:
            return obj


#Создание объявления
class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'boardapp/add.html'
    form_class = AddForm
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        post.author = user
        files = form.cleaned_data['files']  #получаем список файлов
        post.save()
        for f in files:                                 #проверка типа файлов. использую png и mp4 при желании можно добавить больше
            if Path(str(f)).suffix[1:].lower() == 'png':
                Images.objects.create(post=post, image=f).save()
            if Path(str(f)).suffix[1:].lower() == 'mp4':
                v = Video.objects.create(post=post, video=f)
                v.save()
        return super().form_valid(form)


########################################### здесь обитают функции представлений #####################################
@login_required
def add_reply(request, pk):
    if request.method == "POST":
        form = AddReply(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text_reply']
            post = Post.objects.get(pk=pk)
            user = request.user
            rep = PostReply.objects.create(user=user, announce=post, text_reply=text)
            rep.save()
            return redirect("detail", pk=pk)
    else:
        form = AddReply()

    return render(request, 'boardapp/resp.html', {'form': form})


#регистрация
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        form = RegForm(request.POST)
        if form.is_valid():
            confirm_code = code_gen()
            if VerifyUser.objects.filter(username=username):
                old_v = VerifyUser.objects.get(username=username)
                old_v.delete()

            verify_user = VerifyUser.objects.create(username=username, confirm_code=confirm_code,
                                                    password=password, email=email)
            verify_user.save()
            request.session[
                'username'] = username  #запишем в сессию юзернэйм чтоб искать по нему код. не уверен что правильно)
            send_mail(
                "Confirm your account",
                f"Your confirm code:\n {confirm_code}. \n Please enter this code.",
                None,
                [email],
                fail_silently=False,
            )
            return redirect(to='verify')
        return render(request, 'accounts/signup.html', {'form': form})
    else:
        print(request.session)
        form = RegForm
        return render(request, 'accounts/signup.html', {'form': form})


#верификация
def email_verify(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            confirm_code = request.POST['confirm_code']
            user = VerifyUser.objects.get(username=request.session.get('username'))
            if user and confirm_code == user.confirm_code:
                v = user
                u = User.objects.create_user(username=v.username, password=v.password, email=v.email)
                u.save()
                v.delete()
                return redirect(to='login')
    form = VerifyForm
    return render(request, 'accounts/verify.html', {'form': form})


#вход
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return render(request, 'accounts/user_error.html')
        return redirect(to='main')
    if request.method == 'GET':
        form = LoginForm
        return render(request, 'accounts/login.html', {'form': form})


#выход
@login_required
def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect(to='main')
    else:
        return render(request, 'accounts/logout.html')


#принятие отклика
@login_required
def rep_submit(request, pk):
    if request.method == 'POST':
        a = PostReply.objects.get(pk=pk)
        a.submit_reply = True
        a.save()
        return redirect('prof')
    else:
        return render(request, 'boardapp/submit.html')


#удаление отклика
@login_required
def rep_delete(request, pk):
    if request.method == 'POST':
        a = PostReply.objects.get(pk=pk)
        a.delete()
        return redirect('prof')
    else:
        return render(request, 'boardapp/rep_delete.html')


#категории для подписки
@login_required
def subscribe(request):
    if request.method == 'POST':
        cat_list = request.POST.getlist('cat_list')
        for cat in cat_list:
            sub = Subscribers.objects.create(user=request.user, category=cat)
            sub.save()
        return redirect('my_subs')

    category = list(Post.Category)
    sub_cat = Subscribers.objects.filter(user=request.user) #
    un_cat = []                                             #
    for cat in category:                                    # здесь я проверю наличие категории в подписке пользователя
        if not sub_cat.filter(category=cat):                # чтоб её не отображать а то уменя поле unique в модели
            un_cat.append(cat)                              #
    return render(request, 'boardapp/subscribe.html', {'category': un_cat})


#удаление категорий из подписки
@login_required
def unsubscribe(request):
    if request.method == 'POST':
        cat_list = request.POST.getlist('cat_list')
        for cat in cat_list:
            sub = Subscribers.objects.get(user=request.user, category=cat)
            sub.delete()
        return redirect('my_subs')

    subs = Subscribers.objects.filter(user=request.user)
    return render(request, 'boardapp/subs_delete.html', {'subs': subs})


#подписки юзвера
@login_required
def subscriptions(request):
    subs = Subscribers.objects.filter(user=request.user)
    return render(request, 'boardapp/my_subscribe.html', {'subs': subs})


#редирект на главную если юзвер залез куда не надо
def view_404(request, exception):
    return redirect('main')
