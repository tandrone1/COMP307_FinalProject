# Generated by Django 3.0.4 on 2020-04-04 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0010_purchasedlisting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='inventory',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
