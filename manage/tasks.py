from django.core.cache import cache
import requests
import logging
from celery import shared_task
from .models import Mailbox, ClientSecret
from .utils import decrypt_data
import os

logger = logging.getLogger(__name__)


@shared_task
def fetch_tokens(mailbox_id=None):
    logger.info(f"CLIENT_ID: {os.getenv('CLIENT_ID')}")
    logger.info(f"CLIENT_SECRET: {os.getenv('CLIENT_SECRET')}")
    mailboxes = Mailbox.objects.all()

    for mailbox in mailboxes:
        client = mailbox.client
        tenant_id = client.tenant.tenant_id
        client_id = client.client_id
        client_secret = ClientSecret.objects.get(client=client).client_secret

        try:
            # Check if the token already exists in cache
            cache_key = f"token:{tenant_id}:{client_id}:{mailbox.name}"
            if cache.get(cache_key):
                logger.info(f"Token already exists for {mailbox.name}, skipping fetch.")
                continue

            # Fetch token and store it in cache
            token_info = get_access_token(
                tenant_id,
                client_id,
                client_secret,
                mailbox.name,
                mailbox.mailbox_secret,
            )

            access_token = token_info.get("access_token")
            expires_in = int(
                token_info.get("expires_in", 3600)
            )  # Default to 1 hour if not provided

            # Set token in cache for half of its expiration time
            cache.set(cache_key, access_token, timeout=expires_in // 2)

            # Log the token for debugging purposes
            logger.info(f"Token fetched and stored for {mailbox.name}: {access_token}")

        except requests.HTTPError as e:
            logger.error(f"Error fetching token for {mailbox.name}: {str(e)}")
            raise


def get_access_token(tenant_id, client_id, client_secret, username, password):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": decrypt_data(client_secret),
        "resource": "https://graph.microsoft.com",
        "username": username,
        "password": decrypt_data(password),
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Create a Request object
    req = requests.Request("POST", url, data=data, headers=headers)

    # Prepare the request to get the full details (url, headers, body)
    prepared = req.prepare()

    # Log the request details for manual inspection
    logger.info(f"Request URL: {prepared.url}")
    logger.info(f"Request Headers: {prepared.headers}")
    logger.info(f"Request Body: {prepared.body}")

    # Send the request
    session = requests.Session()
    response = session.send(prepared)

    # Check if the request was successful
    if response.status_code != 200:
        logger.error(f"Failed to get token: {response.text}")

    response.raise_for_status()  # This will raise an HTTPError if the response was unsuccessful

    return response.json()
