from django import forms
from .models import ArticleModel, ImageModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class ArticleForm(forms.ModelForm):
    class Meta:
        model = ArticleModel
        fields = ['article_title', 'article_text']


class ArticleImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                'image',
                Submit('submit', 'Submit', css_class='btn btn-outline-maincolor mt-30')
            )
