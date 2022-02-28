# Generated by Django 4.0.2 on 2022-02-28 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(default='Anonymous', max_length=50)),
                ('title', models.CharField(default='No Title', max_length=250)),
                ('number_of_pages', models.IntegerField()),
                ('published_date', models.DateField(default='1970-01-31')),
            ],
        ),
    ]
