from apps.utils.services import get_prefs


def get_site_prefs(request):
    return {k.upper(): v for k, v in get_prefs().items()}
