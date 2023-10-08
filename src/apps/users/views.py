from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView

from .forms import LoginForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import RegisterForm


class UserLoginView(LoginView):
    template_name = 'login.html'
    success_url = '/'


class UserLogoutView(LogoutView):
    success_url_allowed_hosts = '/'


def activate_view(request):
    from .services import activate_user
    token = request.GET.get('token')
    if not token:
        return render(request, 'token_error.html', {'error':  'Invalid Token'})
    else:
        try:
            activate_user(token)
        except Exception as e:
            return render(request, 'token_error.html', {'error':  str(e)})
        return render(request, 'activated.html')


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        from .services import send_activation_email
        send_activation_email(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
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
