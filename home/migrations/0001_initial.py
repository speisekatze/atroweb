# Generated by Django 3.0.7 on 2020-06-06 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('question', models.CharField(max_length=50)),
                ('answer', models.TextField()),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('content', models.TextField()),
                ('status', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('version', models.IntegerField()),
            ],
        ),
    ]
