from django.shortcuts import render
from django.views.generic import ListView
from .models import ArticleModel


class BlogView(ListView):
    model = ArticleModel
    template_name = 'blog.html'
    context_object_name = 'blog'