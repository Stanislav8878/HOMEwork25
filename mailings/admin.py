from django.contrib import admin

from .models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'owner')
    search_fields = ('email', 'full_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'owner')
    search_fields = ('subject',)


class MailingAttemptInline(admin.TabularInline):
    model = MailingAttempt
    extra = 0
    readonly_fields = ('attempted_at', 'status', 'server_response', 'client')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_at', 'end_at', 'status', 'owner')
    list_filter = ('status',)
    inlines = [MailingAttemptInline]


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'client', 'status', 'attempted_at')
    list_filter = ('status',)
