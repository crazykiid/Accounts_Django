# Generated by Django 3.2.4 on 2021-06-29 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsite', '0011_auto_20210629_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='contact',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
