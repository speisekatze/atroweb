# Generated by Django 3.0.7 on 2020-06-22 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp', '0006_auto_20200622_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='session_token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
