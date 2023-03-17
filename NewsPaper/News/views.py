import datetime


from django.http import HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from allauth.account.forms import SignupForm
from django import forms
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin
from .forms import PostForm, SubscribeForm
from .filters import PostFilter
from .models import Post, Author, Subscribers
from django.db.models.signals import post_save
from django.dispatch import receiver




class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


class BaseRegisterView(LoginRequiredMixin, CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/user'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return


def sign(request):
    user = request

    return


class AllList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'timestamp'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'newslist.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 2


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    queryset = Post.objects.filter(content_type=Post.news)
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'timestamp'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'newslist.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 2


class ArticleList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    queryset = Post.objects.filter(content_type=Post.article)
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'timestamp'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'newslist.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 2


class NewsSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'timestamp'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class Article(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'article.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SubscribeForm()
        return context


class ArticleSubscribe(SingleObjectMixin, FormView):
    template_name = 'article.html'
    form_class = SubscribeForm
    model = Post

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        subs = Subscribers()
        user = request.user
        categorys = self.object.category.all()
        subs_list=[]
        for cat in categorys:
            subs_list.append(Subscribers(user=user, category=cat))
        Subscribers.objects.bulk_create(subs_list)
        return super().post(request, *args, **kwargs)



    def get_success_url(self):
        return reverse('article', kwargs={"pk": self.object.pk})


class ArticleView(View):
    def get(self, request, *args, **kwargs):
        view = Article.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ArticleSubscribe.as_view()
        return view(request, *args, **kwargs)


# Добавляем новое представление для создания товаров.
class NewsCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    permission_required = 'News.add_post'
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'


    def form_valid(self, form):
        post = form.save(commit=False)
        post.content_type = Post.news
        post.rating = 0
        post.timestamp = datetime.datetime.now()


        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'News.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.content_type = Post.article
        post.rating = 0
        post.timestamp = datetime.datetime.now()
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'News.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
