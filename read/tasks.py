from celery import shared_task
from manage.models import Mailbox
from .models import ReceivedEmailMessage
from django.core.cache import cache
from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)


@shared_task
def fetch_unread_emails():
    mailboxes = Mailbox.objects.all()  # Get all mailboxes
    for mailbox in mailboxes:

        tenant_id = mailbox.client.tenant.tenant_id  # Correct external tenant ID
        client_id = mailbox.client.client_id  # Correct external client ID

        cache_key = f"token:{tenant_id}:{client_id}:{mailbox.name}"

        access_token = cache.get(cache_key)

        if access_token:
            headers = {"Authorization": f"Bearer {access_token}"}
            url = f"https://graph.microsoft.com/v1.0/users/{mailbox.name}/mailFolders/Inbox/messages?$filter=isRead eq false"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                logger.info("===> Successfully fetched unread emails.")
                emails = response.json().get("value", [])
                for email in emails:
                    message_id = email["id"]

                    # Check if the message already exists in the database
                    if not ReceivedEmailMessage.objects.filter(
                        message_id=message_id
                    ).exists():
                        # Create a new ReceivedEmailMessage object with correct field names
                        ReceivedEmailMessage.objects.create(
                            mailbox=mailbox,
                            message_id=message_id,
                            received_date_time=datetime.strptime(
                                email["receivedDateTime"], "%Y-%m-%dT%H:%M:%SZ"
                            ),
                            subject=email["subject"],
                            has_attachments=email["hasAttachments"],
                            body_content_type=email["body"]["contentType"],
                            body_content=email["body"]["content"],
                            body_preview=email["bodyPreview"],
                            sender_name=email["sender"]["emailAddress"]["name"],
                            sender_address=email["sender"]["emailAddress"]["address"],
                            from_name=email["from"]["emailAddress"]["name"],
                            from_address=email["from"]["emailAddress"]["address"],
                            cc_recipients=email.get("ccRecipients", []),
                            to_recipients=email[
                                "toRecipients"
                            ],  # Assuming this field is JSON
                        )

                    # Mark the email as read in GraphAPI
                    mark_as_read_url = f"https://graph.microsoft.com/v1.0/users/{mailbox.name}/messages/{message_id}"
                    patch_data = {"isRead": True}
                    patch_response = requests.patch(
                        mark_as_read_url, headers=headers, json=patch_data
                    )
                    if patch_response.status_code == 200:
                        # Optionally log or mark success
                        pass
        else:
            logger.info(f"---- Access token not found for {mailbox.name}.")
