# Generated by Django 3.0 on 2020-04-01 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0003_listing_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='edit_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='publish_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
