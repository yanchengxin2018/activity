# Generated by Django 2.0 on 2019-01-17 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190115_0303'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayFinishTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('ip', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='lucktable',
            name='actor_obj',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.ActorTable'),
        ),
    ]
