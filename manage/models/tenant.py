from django.db import models
from django.contrib.auth.models import User

class Tenant(models.Model):
  name = models.CharField(max_length=255, unique=True)
  tenant_id = models.CharField(max_length=255, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL,  null=True, related_name='tenants_created')
  modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tenants_modified')

  def __str__(self):
    return self.name