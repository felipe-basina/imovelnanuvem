# Generated by Django 4.0.6 on 2022-08-11 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inquilinotbl',
            name='dt_vencimento',
        ),
        migrations.AddField(
            model_name='inquilinotbl',
            name='num_vencimento',
            field=models.IntegerField(default=1),
        ),
    ]
