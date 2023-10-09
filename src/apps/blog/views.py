from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .models import ArticleModel, ImageModel
from .forms import ArticleForm


class BlogView(ListView):
    model = ArticleModel
    template_name = 'blog-full.html'
    context_object_name = 'blog'


class AddArticle(CreateView):
    model = ArticleModel
    form_class = ArticleForm
    template_name = 'add_article.html'
    context_object_name = 'add_article'



class ArticleView(DetailView):
    model = ArticleModel
    template_name = 'blog-single-full.html'
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['images'] = self.object.images.all().order_by('index')
        return ctx


class HomeView(ListView):
    model = ArticleModel
    template_name = 'home.html'
    context_object_name = 'home'


