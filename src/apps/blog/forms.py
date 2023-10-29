from django import forms
from .models import ArticleModel, ImageModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from ckeditor.widgets import CKEditorWidget


class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = ArticleModel
        fields = ['article_title', 'content']


class ArticleImageForm(forms.ModelForm):
    article = forms.ModelChoiceField(queryset=ArticleModel.objects.all(), widget=forms.HiddenInput)
    index = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = ImageModel
        fields = ['article', 'image', 'index']
