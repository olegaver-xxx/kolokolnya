from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import ArticleModel


class BlogView(ListView):
    model = ArticleModel
    template_name = 'blog.html'
    context_object_name = 'blog'


class ArticleView(DetailView):
    model = ArticleModel
    template_name = 'detail.html'
    context_object_name = 'detail'
