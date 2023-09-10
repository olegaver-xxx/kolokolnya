from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import ItemModel


class HomeView(TemplateView):
    # template_name = 'base.html'
    ...

class ShopView(ListView):
    template_name = 'base.html'
    context_object_name = 'show'
    model = ItemModel

class ItemView(DetailView):
    ...