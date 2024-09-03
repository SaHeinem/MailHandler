from django.db import models
from django.contrib.auth.models import User
from .tenant import Tenant
from manage.utils import encrypt_data, decrypt_data

class Client(models.Model):
  name = models.CharField(max_length=255)
  client_id = models.CharField(max_length=255)
  tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, related_name='clients')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL,  null=True, related_name='clients_created')
  modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='clients_modified')

  def __str__(self):
    return self.name
  

class ClientSecret(models.Model):
  client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_secrets')
  client_secret = models.CharField(max_length=255)
  valid_until = models.DateField()
  active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL,  null=True, related_name='client_secrets_created')
  modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='client_secrets_modified')

  def __str__(self):
    return self.client.name
  

  def save(self, *args, **kwargs):
    # Invalidate other active secrets for this client
    if self.active:
        ClientSecret.objects.filter(client=self.client, active=True).exclude(id=self.id).update(active=False)

    # Encrypt client secret
    self.client_secret = encrypt_data(self.client_secret)
    super(ClientSecret, self).save(*args, **kwargs)
  
  @property
  def client_secret_decrypt(self):
    return decrypt_data(self.client_secret)