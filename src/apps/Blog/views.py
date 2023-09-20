from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import ArticleModel


class BlogView(ListView):
    model = ArticleModel
    template_name = 'blog-full.html'
    context_object_name = 'blog'


class ArticleView(DetailView):
    model = ArticleModel
    template_name = 'blog-single-full.html'
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        ctx = super(ArticleModel).get_context_data(**kwargs)
        ctx['article_image'] = self.object
        ctx['article_image'] = self.object.image_set.all().order_by('GalleryImage__index')
        return ctx

class HomeView(ListView):
    model = ArticleModel
    template_name = 'home.html'
    context_object_name = 'home'


