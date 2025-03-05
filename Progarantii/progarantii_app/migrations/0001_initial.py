# Generated by Django 5.1.6 on 2025-02-27 11:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, unique=True, verbose_name='Полное название')),
                ('short_name', models.CharField(blank=True, max_length=25, verbose_name='Короткое название')),
                ('AKRA_rating', models.CharField(blank=True, choices=[('AAA(RU)', 'AAA(RU)'), ('AA+(RU)', 'AA+(RU)'), ('AA(RU)', 'AA(RU)'), ('AA-(RU)', 'AA-(RU)'), ('A+(RU)', 'A+(RU)'), ('A+(RU)', 'A+(RU)'), ('A(RU)', 'A(RU)'), ('A-(RU)', 'A-(RU)'), ('BBB+(RU)', 'BBB+(RU)'), ('BBB+(RU)', 'BBB+(RU)'), ('BBB(RU)', 'BBB(RU)'), ('BBB-(RU)', 'BBB-(RU)'), ('BB+(RU)', 'BB+(RU)'), ('BB+(RU)', 'BB+(RU)'), ('BB(RU)', 'BB(RU)'), ('BB-(RU)', 'BB-(RU)'), ('B+(RU)', 'B+(RU)'), ('B(RU)', 'B(RU)'), ('B-(RU)', 'B-(RU)')], max_length=20, verbose_name='Рейтинг АКР')),
                ('Expert_RA', models.CharField(blank=True, choices=[('ruAAA', 'ruAAA'), ('ruAA+', 'ruAA+'), ('ruAA', 'ruAA'), ('ruAA-', 'ruAA-'), ('ruA+', 'ruA+'), ('ruA', 'ruA'), ('ruA-', 'ruA-'), ('ruBBB+', 'ruBBB+'), ('ruBBB', 'ruBBB'), ('ruBBB-', 'ruBBB-'), ('ruBB+', 'ruBB+'), ('ruBB', 'ruBB'), ('ruBB-', 'ruBB-'), ('ruB+', 'ruB+'), ('ruB', 'ruB'), ('ruB-', 'ruB-')], max_length=20, verbose_name='Рейтинг Эксперт РА')),
            ],
        ),
        migrations.CreateModel(
            name='DateRangeName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Guarantee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_guarantee', models.CharField(blank=True, choices=[('Участие', 'Участие'), ('Исполнение', 'Исполнение'), ('Гарантийные обязательства', 'Гарантийные обязательства')], max_length=50, verbose_name='Тип гарантии')),
            ],
        ),
        migrations.CreateModel(
            name='Law',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_law', models.CharField(blank=True, choices=[('№ 44', '№ 44'), ('№ 223', '№ 223'), ('№ 615', '№ 615'), ('ком', 'ком')], max_length=50, verbose_name='Тип закона')),
            ],
        ),
        migrations.CreateModel(
            name='PriceRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_price', models.PositiveIntegerField(verbose_name='От')),
                ('end_price', models.PositiveIntegerField(verbose_name='До')),
            ],
        ),
        migrations.CreateModel(
            name='PriceRangeName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DateRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.PositiveIntegerField(verbose_name='Дата начало')),
                ('end_date', models.PositiveIntegerField(verbose_name='Дата конец')),
                ('date_range_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='progarantii_app.daterangename', verbose_name='Название диапазона')),
            ],
        ),
        migrations.CreateModel(
            name='PossibleRangePrices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('have_advance', models.BooleanField(blank=True, default=False, null=True, verbose_name='Аванс')),
                ('bank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='progarantii_app.bank', verbose_name='Банк')),
                ('date_range_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='progarantii_app.daterangename', verbose_name='Диапазон дат')),
                ('guarantee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='progarantii_app.guarantee', verbose_name='Гарантия')),
                ('law', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='progarantii_app.law', verbose_name='Закон')),
                ('price_range_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='progarantii_app.pricerangename', verbose_name='Диапазон цен')),
            ],
        ),
        migrations.CreateModel(
            name='BaseBanksPrices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_percent', models.PositiveIntegerField(blank=True, null=True, verbose_name='Процент %')),
                ('date_range', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='progarantii_app.daterange', verbose_name='Диапазон дат')),
                ('possible_range_prices', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='progarantii_app.possiblerangeprices')),
                ('price_range', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='progarantii_app.pricerange', verbose_name='Диапазон цен')),
            ],
        ),
        migrations.AddField(
            model_name='pricerange',
            name='price_range_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='progarantii_app.pricerangename', verbose_name='Название диапазона'),
        ),
    ]
