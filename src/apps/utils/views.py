from django.contrib import admin
from django.views.generic import TemplateView, ListView
from apps.utils.services import get_prefs_form, set_prefs
from django.http import HttpResponseForbidden
from .models import MainGallery


class PreferencesView(TemplateView):
    template_name = 'prefs.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(PreferencesView, self).get_context_data(**kwargs)
        ctx.update(admin.site.each_context(self.request))
        ctx['prefs'] = get_prefs_form()
        return ctx

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        set_prefs(data)
        return self.get(request, *args, **kwargs)


class MainView(ListView):
    template_name = 'index.html'
    model = MainGallery
    context_object_name = 'images'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = MainGallery.objects.order_by('index')
        return qs