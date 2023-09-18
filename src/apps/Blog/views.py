from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import ArticleModel


class BlogView(ListView):
    model = ArticleModel
    template_name = 'blog-full.html'
    context_object_name = 'blog'


class ArticleView(DetailView):
    model = ArticleModel
    # template_name = 'blog.html'
    context_object_name = 'model'


class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'home'
    model = ArticleModel