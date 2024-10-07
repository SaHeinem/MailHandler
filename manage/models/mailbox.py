from django.db import models
from django.contrib.auth.models import User
from .client import Client
from .jira import JiraIssueType, JiraProject
from manage.utils import encrypt_data, decrypt_data


class Mailbox(models.Model):
    name = models.CharField(max_length=255)
    mailbox_secret = models.CharField(max_length=255)
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, related_name="mailboxes"
    )
    default_jira_project = models.ForeignKey(
        JiraProject, on_delete=models.PROTECT, related_name="mailboxes"
    )
    default_jira_issue_type = models.ForeignKey(
        JiraIssueType, on_delete=models.PROTECT, related_name="mailboxes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="mailboxes_created"
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mailboxes_modified",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "mailboxes"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.mailbox_secret = encrypt_data(self.mailbox_secret)
        super(Mailbox, self).save(*args, **kwargs)

    @property
    def mailbox_secret_decrypt(self):
        return decrypt_data(self.mailbox_secret)


# class Alias(models.Model):
#     alias = models.CharField(max_length=255)
#     mailbox = models.ForeignKey(
#         Mailbox, on_delete=models.CASCADE, related_name="aliases"
#     )
#     default_jira_project = models.ForeignKey(
#         JiraProject, on_delete=models.PROTECT, related_name="mailboxes"
#     )
#     default_jira_issue_type = models.ForeignKey(
#         JiraIssueType, on_delete=models.PROTECT, related_name="mailboxes"
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, related_name="aliases_created"
#     )
#     modified_by = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="aliases_modified",
#     )

#     class Meta:
#         verbose_name_plural = "aliases"

#     def __str__(self):
#         return self.alias
