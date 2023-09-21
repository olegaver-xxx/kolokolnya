from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, RegistrationForm


class LoginView(View):
    def get(self, request):
        return render(request, 'shop-account-login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('products:product_list')
        return render(request, 'shop-account-login.html', {'form': form})


# class RegistrationView(View):
#     def get(self, request):
#         return render(request, 'users/registration.html', {'form': RegistrationForm()})
#
#     def post(self, request):
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('users:login')
#         return render(request, 'users/registration.html', {'form': form})