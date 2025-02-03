# Generated by Django 4.2.15 on 2024-09-23 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_usersubscriptionmodel_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionsmodel',
            name='price',
        ),
        migrations.AddField(
            model_name='subscriptionsmodel',
            name='discont_monthly',
            field=models.IntegerField(default=0, null=True, verbose_name='خصم'),
        ),
        migrations.AddField(
            model_name='subscriptionsmodel',
            name='discont_yearly',
            field=models.IntegerField(default=0, null=True, verbose_name='خصم'),
        ),
        migrations.AddField(
            model_name='subscriptionsmodel',
            name='plan_type',
            field=models.CharField(choices=[('premium', 'Premium'), ('pro', 'PRO'), ('basic', 'Basic')], max_length=255, null=True, verbose_name='نو الاشتراك'),
        ),
        migrations.AddField(
            model_name='subscriptionsmodel',
            name='price_monthly',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='السعر'),
        ),
        migrations.AddField(
            model_name='subscriptionsmodel',
            name='price_yearly',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True, verbose_name='السعر'),
        ),
        migrations.AlterField(
            model_name='subscriptionsmodel',
            name='Theem',
            field=models.CharField(choices=[('primary', 'primary'), ('secondary', 'secondary'), ('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('info', 'info'), ('light', 'light'), ('dark', 'dark')], max_length=255, null=True, verbose_name='الثيم'),
        ),
    ]
