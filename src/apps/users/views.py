from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import LoginForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import RegisterForm
from .models import User, Profile
from django.http import JsonResponse
from . import services as user_services
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, UserPasswordChangeForm


class UserLoginView(LoginView):
    template_name = 'login.html'
    success_url = '/profile'


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


class ProfileView(TemplateView):
    template_name = 'profile.html'

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data
    #     ctx['profile'] = self.request.user.profile
    #     return ctx


@login_required
def update_user(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = UserPasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = UserPasswordChangeForm(request.user)
    return render(request, 'edit_user_info.html', {'user_form': user_form, 'password_form': password_form})
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
