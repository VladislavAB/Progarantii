from django.db import models


# Create your models here.
class Bank(models.Model):
    AKRA_RATING = [('AAA(RU)', 'AAA(RU)'), ('AA+(RU)', 'AA+(RU)'), ('AA(RU)', 'AA(RU)'), ('AA-(RU)', 'AA-(RU)'),
                   ('A+(RU)', 'A+(RU)'), ('A+(RU)', 'A+(RU)'), ('A(RU)', 'A(RU)'), ('A-(RU)', 'A-(RU)'),
                   ('BBB+(RU)', 'BBB+(RU)'), ('BBB+(RU)', 'BBB+(RU)'), ('BBB(RU)', 'BBB(RU)'), ('BBB-(RU)', 'BBB-(RU)'),
                   ('BB+(RU)', 'BB+(RU)'), ('BB+(RU)', 'BB+(RU)'), ('BB(RU)', 'BB(RU)'), ('BB-(RU)', 'BB-(RU)'),
                   ('B+(RU)', 'B+(RU)'), ('B(RU)', 'B(RU)'), ('B-(RU)', 'B-(RU)')]
    EXPERT_RA = [('ruAAA', 'ruAAA'), ('ruAA+', 'ruAA+'), ('ruAA', 'ruAA'), ('ruAA-', 'ruAA-'), ('ruA+', 'ruA+'),
                 ('ruA', 'ruA'), ('ruA-', 'ruA-'), ('ruBBB+', 'ruBBB+'), ('ruBBB', 'ruBBB'), ('ruBBB-', 'ruBBB-'),
                 ('ruBB+', 'ruBB+'), ('ruBB', 'ruBB'), ('ruBB-', 'ruBB-'), ('ruB+', 'ruB+'), ('ruB', 'ruB'),
                 ('ruB-', 'ruB-')]
    full_name = models.CharField(max_length=255, unique=True, verbose_name='Полное название')
    short_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Короткое название')
    AKRA_rating = models.CharField(max_length=50, choices=AKRA_RATING, blank=True, verbose_name='Рейтинг АКР')
    Expert_RA = models.CharField(max_length=50, choices=EXPERT_RA, blank=True, null=True,
                                 verbose_name='Рейтинг Эксперт РА')

    def __str__(self):
        return self.full_name


class Law(models.Model):
    TYPES_OF_LAW = [('№ 44', '№ 44'),
                    ('№ 223', '№ 223'),
                    ('№ 615', '№ 615'),
                    ('ком', 'ком')]
    type_of_law = models.CharField(max_length=50, choices=TYPES_OF_LAW, blank=True, null=True,
                                   verbose_name='Тип закона')

    def __str__(self):
        return f'Закон {self.type_of_law}'


class Guarantee(models.Model):
    TYPES_OF_GUARANTEE = [
        ('Участие', 'Участие'), ('Исполнение', 'Исполнение'),
        ('Гарантийные обязательства', 'Гарантийные обязательства')]

    type_of_guarantee = models.CharField(max_length=50, choices=TYPES_OF_GUARANTEE, blank=True, null=True,
                                         verbose_name='Тип гарантии')

    def __str__(self):
        return f'{self.type_of_guarantee}'


class DateRangeName(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=True, null=True, verbose_name="Имя диапазона")

    def __str__(self):
        return f'{self.name} дней'


class DateRange(models.Model):
    start_date = models.PositiveIntegerField(verbose_name='Дата начало')
    end_date = models.PositiveIntegerField(verbose_name='Дата конец')
    date_range_name = models.ForeignKey("DateRangeName", on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='Название диапазона')

    def __str__(self):
        return f'{self.start_date} - {self.end_date} дней'


class PriceRangeName(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=True, null=True, verbose_name="Имя диапазона")

    def __str__(self):
        return f'Диапазон {self.name}'


class PriceRange(models.Model):
    start_price = models.PositiveIntegerField(verbose_name='От')
    end_price = models.PositiveIntegerField(verbose_name='До')
    price_range_name = models.ForeignKey("PriceRangeName", on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name='Название диапазона')

    def __str__(self):
        return f'{self.start_price} - {self.end_price}'


class PossibleRangePrices(models.Model):
    bank = models.ForeignKey("Bank", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Банк")
    law = models.ForeignKey("Law", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Закон")
    guarantee = models.ForeignKey("Guarantee", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Гарантия")
    have_advance = models.BooleanField(default=False, blank=True, null=True, verbose_name='Аванс')
    date_range_name = models.ForeignKey("DateRangeName", on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="Диапазон дат")
    price_range_name = models.ForeignKey("PriceRangeName", on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name="Диапазон цен")

    def __str__(self):
        return (f'{self.bank} | {self.law} | {self.guarantee} | {self.date_range_name} | {self.price_range_name}'
                f' | Аванс: {self.have_advance}')


class BaseBanksPrices(models.Model):
    possible_range_prices = models.ForeignKey("PossibleRangePrices", null=True, blank=True, on_delete=models.CASCADE)
    price_range = models.ForeignKey("PriceRange", on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="Диапазон цен")
    date_range = models.ForeignKey("DateRange", on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="Диапазон дат")
    year_percent = models.PositiveIntegerField(null=True, blank=True, verbose_name="Процент %")
