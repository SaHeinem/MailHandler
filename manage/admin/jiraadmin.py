from django.contrib import admin
from manage.models import JiraTenant, JiraProject, JiraIssueType
from manage.forms import JiraTenantForm
from manage.utils import set_user_audit_fields


# Register your models here.
class JiraTenantAdmin(admin.ModelAdmin):
    form = JiraTenantForm
    list_display = ("name", "tenant", "created_at", "updated_at")
    search_fields = ("name", "tenant")
    readonly_fields = ("created_at", "updated_at", "created_by", "modified_by")

    def save_model(self, request, obj, form, change):
        set_user_audit_fields(request, obj, change)
        super().save_model(request, obj, form, change)


admin.site.register(JiraTenant, JiraTenantAdmin)


class JiraProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "jira_tenant", "created_at", "updated_at")
    search_fields = ("name", "jira_tenant__name")
    readonly_fields = ("created_at", "updated_at", "created_by", "modified_by")

    def save_model(self, request, obj, form, change):
        set_user_audit_fields(request, obj, change)
        super().save_model(request, obj, form, change)


admin.site.register(JiraProject, JiraProjectAdmin)


class JiraIssueTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "get_jira_projects", "created_at", "updated_at")
    search_fields = ("name", "jira_projects__name")
    readonly_fields = ("created_at", "updated_at", "created_by", "modified_by")

    def save_model(self, request, obj, form, change):
        set_user_audit_fields(request, obj, change)
        super().save_model(request, obj, form, change)

    def get_jira_projects(self, obj):
        return ", ".join([project.name for project in obj.jira_projects.all()])

    get_jira_projects.short_description = "Jira Projects"


admin.site.register(JiraIssueType, JiraIssueTypeAdmin)
