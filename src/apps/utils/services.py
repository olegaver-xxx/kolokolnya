from copy import deepcopy


def list_images():
    pass


PREFS = {
    'contact_phone': dict(label='Contact Phone', value='000000000000', type=str),
    'contact_email': dict(label='Contact Email', value='', type=str),
    'disable_shop': dict(label='Disable Shop', value=False, type=bool),
    'enable_blog': dict(label='Enable Blog', value=True, type=bool),
    'header_image': dict(label='Header Image', value='images/hiero.png', type=str, choices=list_images),
    'site_name': dict(label='Site Name', value='Kolokolnya', type=str),
    'yookassa_apikey': dict(label='Yookassa API Key', value='', type=str),
    'yookassa_secretkey': dict(label='Yookassa Secret Key', value='', type=str),
}


def get_prefs_model():
    from .models import Preferences
    return Preferences.objects.get_or_create()[0]


def get_prefs():
    return get_prefs_model().prefs


def validate_prefs(prefs):
    """
    {'key': 123}
    """
    for field, value in prefs.items():
        prefs[field] = PREFS[field]['type'](value)
    return prefs


def set_prefs(prefs: dict):
    prefs = validate_prefs(prefs)
    prefs_model = get_prefs_model()
    prefs_model.prefs = prefs
    prefs_model.save()


def get_value(key: str, default=None):
    return get_prefs().get(key, default)


def set_value(key: str, value: any):
    model = get_prefs_model()
    model.prefs[key] = value
    model.save()


def get_prefs_form():
    """
    [
        {label: 'Test', name: 'test', value: 0, type: int},
    ]
    """
    prefs = get_prefs()
    fields = deepcopy(PREFS)

    for field, values in fields.items():
        values['value'] = prefs.get(field)
        values['type'] = values['type'].__name__
    return fields


def get_text_block_content(block_name):
    from .models import TextBlockModel
    try:
        return TextBlockModel.objects.get(name=block_name).text
    except TextBlockModel.DoesNotExist:
        return ''
