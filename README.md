# Django Mail to Jira Automation

This Django application integrates with Microsoft Graph API to read emails and automatically create or update Jira tickets based on email content. The app can reply to emails automatically and supports sending emails from shared mailboxes.

## Features
- Email to Jira Ticket Creation: Automatically create Jira tickets from incoming emails.
- Reply Handling: Add comments to existing Jira tickets if an email replies to a ticket key.
- Auto-Reply: Automatically send replies to new Jira tickets.
- Shared Mailbox Support: Send emails from shared mailboxes.


## Getting Started
### Prerequisites
Before running this app, ensure you have the following services running:

- A PostgreSQL database
- A Redis server (or a compatible drop-in replacement)
  - separating the cache and celery into two shards is necessary


### Setup
1. Clone the repository
2. Copy the environment file and configure your environment:
```bash
cp .env.example .env
```
You'll need to generate a 32-character URL-safe base64-encoded 
string for the SECRET_KEY. You can generate it [here](https://8gwifi.org/fernet.jsp).

3. Run the application in Docker:

The repository includes a Docker setup for development purposes.
```bash
docker-compose up
```
This will start the Django application along with any necessary dependencies.

## Usage
- Automatic Jira Ticket Creation: Incoming emails will automatically create Jira tickets if they do not reference an existing ticket key.
- Commenting on Existing Tickets: Replies to emails containing a Jira ticket key will be added as comments to the corresponding Jira ticket.
- Auto-Reply to New Tickets: The application will automatically reply to the sender when a new Jira ticket is created.

## Running in Development
The app is set up with Docker for easy development. Just run docker-compose up to start the app and its dependencies.

You can interact with the app via the Django admin panel or by configuring your mail client to send test emails to the monitored inbox.

## License
This project is licensed under a private license. All rights are reserved.