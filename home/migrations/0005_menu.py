# Generated by Django 3.0.7 on 2020-06-07 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_faq_sort'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
                ('url', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=1)),
                ('sort', models.IntegerField(default=1)),
            ],
        ),
    ]
