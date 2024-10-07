from django.contrib import admin
from .models import ReceivedEmailMessage


# Register your models here.
class ReceivedEmailMessageAdmin(admin.ModelAdmin):
    list_filter = ("mailbox",)
    list_display = (
        "subject",
        "received_date_time",
        "sender_name",
        "sender_address",
        "from_name",
        "from_address",
        "mailbox",
    )
    search_fields = (
        "subject",
        "sender_name",
        "sender_address",
        "from_name",
        "from_address",
    )


admin.site.register(ReceivedEmailMessage, ReceivedEmailMessageAdmin)
