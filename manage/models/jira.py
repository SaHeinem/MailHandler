from django.db import models
from django.contrib.auth.models import User
from manage.utils import encrypt_data, decrypt_data


class JiraTenant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    tenant = models.CharField(max_length=255, unique=True)
    default_user_mail = models.CharField(max_length=255)
    default_user_token = models.CharField(max_length=510)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="jira_tenants_created"
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jira_tenants_modified",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.default_user_token = encrypt_data(self.default_user_token)
        super(JiraTenant, self).save(*args, **kwargs)

    @property
    def default_user_token_decrypt(self):
        return decrypt_data(self.default_user_token)


class JiraProject(models.Model):
    name = models.CharField(max_length=255)
    project_key = models.CharField(max_length=255)
    project_id = models.CharField(max_length=255)
    jira_tenant = models.ForeignKey(
        JiraTenant, on_delete=models.CASCADE, related_name="jira_projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="jira_projects_created"
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jira_projects_modified",
    )

    def __str__(self):
        return self.name


class JiraIssueType(models.Model):
    name = models.CharField(max_length=255)
    issuetype_id = models.CharField(max_length=255)
    jira_projects = models.ManyToManyField(JiraProject, related_name="jira_issue_types")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="jira_issue_types_created",
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jira_issue_types_modified",
    )

    def __str__(self):
        return self.name
