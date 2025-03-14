# Generated by Django 5.1.6 on 2025-03-12 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progarantii_app', '0002_rename_basebanksprices_basebankpercent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='license_number',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер лицензии'),
        ),
        migrations.AddField(
            model_name='bank',
            name='url',
            field=models.URLField(blank=True, null=True, unique=True, verbose_name='Ссылка'),
        ),
    ]
