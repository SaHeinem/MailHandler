from django import forms
from .models import Mailbox, ClientSecret, JiraTenant
from django.forms import PasswordInput

class MailboxForm(forms.ModelForm):
    class Meta:
        model = Mailbox
        fields = '__all__'
        widgets = {
            'mailbox_secret': PasswordInput(render_value=True),
        }

class ClientSecretForm(forms.ModelForm):
    class Meta:
        model = ClientSecret
        fields = '__all__'
        widgets = {
            'client_secret': PasswordInput(render_value=True),
        }

class JiraTenantForm(forms.ModelForm):
    class Meta:
        model = JiraTenant
        fields = '__all__'
        widgets = {
            'default_user_token': PasswordInput(render_value=True),
        }
        