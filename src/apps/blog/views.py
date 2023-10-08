from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .models import ArticleModel, ImageModel


class BlogView(ListView):
    model = ArticleModel
    template_name = 'blog-full.html'
    context_object_name = 'blog'


# class CreateArticleView(PermissionRequiredMixin, CreateView):
#     permission_required = ['blog.add_articlemodel']
#     template_name = ''
#
#     def get(self, request):
#         ...
#
#     def post(self, request, *args, **kwargs):
#         pass


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


