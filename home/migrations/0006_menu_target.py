# Generated by Django 3.0.7 on 2020-06-07 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='target',
            field=models.CharField(default='_self', max_length=50),
        ),
    ]