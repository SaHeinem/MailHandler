# Generated by Django 5.1.1 on 2024-10-08 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivedemailmessage',
            name='cc_recipients',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
