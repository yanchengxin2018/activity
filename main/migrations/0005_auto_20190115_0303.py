# Generated by Django 2.0 on 2019-01-15 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_actortable_lucked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actortable',
            name='lucked',
        ),
        migrations.AddField(
            model_name='actortable',
            name='is_first',
            field=models.BooleanField(default=True),
        ),
    ]
