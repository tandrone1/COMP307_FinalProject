# Generated by Django 3.0 on 2020-04-16 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200416_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='username',
            field=models.CharField(default='delete', max_length=100),
        ),
    ]
