# Generated by Django 4.2.15 on 2024-09-17 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_subscriptionsmodel_usersubscriptionmodel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='subscription',
        ),
        migrations.AddField(
            model_name='hospitalsmodel',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.usersubscriptionmodel'),
        ),
    ]
