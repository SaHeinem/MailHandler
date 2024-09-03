from django.contrib import admin
from django.contrib import messages
from manage.models import Tenant, Client, ClientSecret, Mailbox, Alias
from manage.forms import MailboxForm, ClientSecretForm
from manage.utils import set_user_audit_fields
from manage.tasks import fetch_tokens


# Register your models here.
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "tenant_id", "created_at", "updated_at")
    search_fields = ("name", "tenant_id")
    readonly_fields = ("created_at", "updated_at", "created_by", "modified_by")

    def save_model(self, request, obj, form, change):
        set_user_audit_fields(request, obj, change)
        super().save_model(request, obj, form, change)


admin.site.register(Tenant, TenantAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "client_id", "tenant", "created_at", "updated_at")
    search_fields = ("name", "client_id", "tenant__name")
    readonly_fields = ("created_at", "updated_at", "created_by", "modified_by")

    def save_model(self, request, obj, form, change):
        set_user_audit_fields(request, obj, change)
        super().save_model(request, obj, form, change)


admin.site.register(Client, ClientAdmin)


class ClientSecretAdmin(admin.ModelAdmin):
    form = ClientSecretForm
    list_display = ("client", "valid_until", "active", "created_at", "updated_at")
    search_fields = ("client__name",)
    readonly_fields = ("created_at", "updated_at", "created_by", "modified_by")

    def get_exclude(self, request, obj=None):
        if (
            obj
        ):  # This means the object is being updated, so exclude the client_secret field
            return ("client_secret",)
        return self.exclude

    def save_model(self, request, obj, form, change):
        set_user_audit_fields(request, obj, change)
        super().save_model(request, obj, form, change)


admin.site.register(ClientSecret, ClientSecretAdmin)


class MailboxAdmin(admin.ModelAdmin):
    form = MailboxForm
    list_display = (
        "name",
        "client",
        "default_jira_issue_type",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "client__name")
    readonly_fields = ("created_at", "updated_at", "created_by", "modified_by")
    actions = ["trigger_fetch_tokens"]

    def trigger_fetch_tokens(self, request, queryset):
        for mailbox in queryset:
            fetch_tokens.delay(mailbox.id)
            messages.success = f"Triggered fetch_tokens for mailbox {mailbox.name}"

    trigger_fetch_tokens.short_description = "Trigger fetch_tokens"

    def save_model(self, request, obj, form, change):
        set_user_audit_fields(request, obj, change)
        super().save_model(request, obj, form, change)


admin.site.register(Mailbox, MailboxAdmin)


class AliasAdmin(admin.ModelAdmin):
    list_display = ("alias", "mailbox", "created_at", "updated_at")
    search_fields = ("alias", "mailbox__name")
    readonly_fields = ("created_at", "updated_at", "created_by", "modified_by")

    def save_model(self, request, obj, form, change):
        set_user_audit_fields(request, obj, change)
        super().save_model(request, obj, form, change)


admin.site.register(Alias, AliasAdmin)
