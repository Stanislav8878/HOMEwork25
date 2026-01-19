from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import UserRegisterForm, UserLoginForm, UserProfileForm

User = get_user_model()


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Отправка приветственного письма
        user = self.object
        if user.email:
            send_mail(
                subject='Добро пожаловать в SkyStore',
                message='Спасибо за регистрацию в SkyStore!',
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                recipient_list=[user.email],
                fail_silently=True,
            )

        return response


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = UserLoginForm


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:home')


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        # редактируем текущего пользователя
        return self.request.user
