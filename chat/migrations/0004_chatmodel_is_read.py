# Generated by Django 4.1.4 on 2023-07-16 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chatmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='is_read',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
