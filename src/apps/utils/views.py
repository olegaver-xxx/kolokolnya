from django.contrib import admin
from django.views.generic import TemplateView
from apps.utils.services import get_prefs_form, set_prefs


class PreferencesView(TemplateView):
    template_name = 'prefs.html'

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
