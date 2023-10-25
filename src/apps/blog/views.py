from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .models import ArticleModel, ImageModel
from .forms import ArticleForm, ArticleImageForm
from apps.users.models import User
from django.urls import reverse


class BlogView(ListView):
    model = ArticleModel
    template_name = 'blog-full.html'
    context_object_name = 'articles'

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.filter(images__image=self.model.images)
    #     return qs


class AddArticle(CreateView):
    model = ArticleModel
    form_class = ArticleForm
    template_name = 'add_article.html'
    context_object_name = 'add_article'
    prefix = 'article'
    success_url = '/blog/'


    def get_success_url(self):
        return reverse('article', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_article'] = self.get_form()
        ctx['form_images'] = [ArticleImageForm(prefix=f'images-{i}', initial={'index': i}) for i in range(5)]
        return ctx

    def form_valid(self, form):
        res = super().form_valid(form)
        for i in range(5):
            form_image = ArticleImageForm(
                {f'images-{i}-article': self.object.id, f'images-{i}-index': i},
                self.request.FILES,
                prefix=f'images-{i}',
            )
            if form_image.is_valid():
                if form_image.cleaned_data['image']:
                    form_image.save()
        return res


class ArticleView(DetailView):
    model = ArticleModel
    template_name = 'blog-single-full.html'
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['images'] = self.object.images.all().order_by('index', 'id')
        return ctx


class HomeView(TemplateView):
    template_name = 'home.html'

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data()
    #     ctx['email'] = self.request.user.email
    #     return ctx


def header(render, request):
    email = User.email
    context = {
        'email': email,
    }
    render(request, 'head-panel.html', context)
