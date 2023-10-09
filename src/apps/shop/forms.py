from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from .models import Product, ProductImage
#
#
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'description', 'price']
#
#
# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = ProductImage
#         fields = ['image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


class ImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'image',
            # Submit('submit', 'Submit', css_class='btn btn-outline-maincolor mt-30')
        )