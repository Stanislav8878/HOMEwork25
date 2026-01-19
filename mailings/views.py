from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import ClientForm, MessageForm, MailingForm
from .models import Client, Message, Mailing, MailingAttempt
from .services import send_mailing


class OwnerQuerysetMixin:
    """
    Ограничивает queryset объектами текущего пользователя.
    Менеджерам с правом self.manager_perm показываем все.
    """
    owner_field = 'owner'
    manager_perm = None  # пример: 'mailings.view_all_clients'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if self.manager_perm and user.has_perm(self.manager_perm):
            return qs
        return qs.filter(**{self.owner_field: user})


# ----- Клиенты -----

class ClientListView(LoginRequiredMixin, OwnerQuerysetMixin, ListView):
    model = Client
    template_name = 'mailings/client_list.html'
    context_object_name = 'clients'
    manager_perm = 'mailings.view_all_clients'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, OwnerQuerysetMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')
    manager_perm = 'mailings.view_all_clients'


class ClientDeleteView(LoginRequiredMixin, OwnerQuerysetMixin, DeleteView):
    model = Client
    template_name = 'mailings/client_confirm_delete.html'
    success_url = reverse_lazy('mailings:client_list')
    manager_perm = 'mailings.view_all_clients'


# ----- Сообщения -----

class MessageListView(LoginRequiredMixin, OwnerQuerysetMixin, ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'messages'
    manager_perm = 'mailings.view_all_messages'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, OwnerQuerysetMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')
    manager_perm = 'mailings.view_all_messages'


class MessageDeleteView(LoginRequiredMixin, OwnerQuerysetMixin, DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')
    manager_perm = 'mailings.view_all_messages'


# ----- Рассылки -----

class MailingListView(LoginRequiredMixin, OwnerQuerysetMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'
    manager_perm = 'mailings.view_all_mailings'


class MailingDetailView(LoginRequiredMixin, OwnerQuerysetMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'
    manager_perm = 'mailings.view_all_mailings'

    def get_queryset(self):
        # подключаем related для попыток
        qs = super().get_queryset()
        return qs.prefetch_related('clients', 'attempts')


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, OwnerQuerysetMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')
    manager_perm = 'mailings.view_all_mailings'


class MailingDeleteView(LoginRequiredMixin, OwnerQuerysetMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')
    manager_perm = 'mailings.view_all_mailings'


# ----- Попытки рассылок -----

class AttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailings/attempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        qs = super().get_queryset().select_related('mailing', 'client', 'mailing__owner')
        user = self.request.user
        if user.has_perm('mailings.view_all_mailings'):
            return qs
        return qs.filter(mailing__owner=user)


# ----- Отправка рассылки -----

@login_required
def send_mailing_view(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    if (
        mailing.owner != request.user
        and not request.user.has_perm('mailings.view_all_mailings')
    ):
        return redirect('mailings:mailing_list')

    send_mailing(mailing)
    return redirect('mailings:mailing_detail', pk=pk)
