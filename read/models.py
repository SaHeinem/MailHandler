from django.db import models


class ReceivedEmailMessage(models.Model):
    mailbox = models.ForeignKey(
        "manage.Mailbox", on_delete=models.PROTECT, related_name="received_emails"
    )
    # Basic message details
    message_id = models.CharField(max_length=255, unique=True)
    received_date_time = models.DateTimeField()
    subject = models.CharField(max_length=255)
    has_attachments = models.BooleanField()

    # Body fields
    body_content_type = models.CharField(max_length=50)
    body_content = models.TextField()
    body_preview = models.TextField()

    # Sender details
    sender_name = models.CharField(max_length=255)
    sender_address = models.EmailField()

    # From details (could be the same as sender)
    from_name = models.CharField(max_length=255)
    from_address = models.EmailField()

    # To recipients (this could be a foreign key to another model or a JSON field)
    to_recipients = models.JSONField()

    # Cc recipients (this could be a foreign key to another model or a JSON field)
    cc_recipients = models.JSONField()

    jiraissueid = models.CharField(max_length=255, null=True)
    is_ticket_trigger = models.BooleanField(default=True)

    def __str__(self):
        return f"Received Email: {self.subject}"
