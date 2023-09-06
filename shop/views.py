from django.shortcuts import render
from django.views.generic import TemplateView, ListView


class HomeView(TemplateView):
    template_name = 'base.html'


class ShopView(ListView):
    ...

