# Generated by Django 3.0.2 on 2020-01-17 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sniping_site', '0003_auto_20200117_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='entrytime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='showtime',
            field=models.DateTimeField(null=True),
        ),
    ]
