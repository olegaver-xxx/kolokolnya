from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm, RegistrationForm


class UserLoginView(LoginView):
    template_name = 'login.html'
    success_url = '/'

class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'





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