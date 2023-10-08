from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import RegisterForm


class UserLoginView(LoginView):
    template_name = 'login.html'
    success_url = '/'


class UserLogoutView(LogoutView):
    success_url_allowed_hosts = '/'


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


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
