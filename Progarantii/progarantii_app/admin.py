from django.contrib import admin
from . import models
from django import forms  # Добавил новое


@admin.register(models.Bank)
class BankAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'short_name']
    list_display = ['full_name', 'short_name', 'AKRA_rating', 'Expert_RA']
    list_editable = ['AKRA_rating', 'Expert_RA']


@admin.register(models.Law)
class LawAdmin(admin.ModelAdmin):
    list_display = ['type_of_law']


@admin.register(models.Guarantee)
class GuaranteeAdmin(admin.ModelAdmin):
    list_display = ['type_of_guarantee']


@admin.register(models.DateRange)
class DateRangeAdmin(admin.ModelAdmin):
    ordering = ['start_date']
    list_display = ['__str__', 'date_range_name']
    list_editable = ['date_range_name']


@admin.register(models.DateRangeName)
class DateRangeNameAdmin(admin.ModelAdmin):
    list_display = ['__str__']


@admin.register(models.PriceRange)
class PriceRangeAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['__str__', 'price_range_name']
    list_editable = ['price_range_name']


@admin.register(models.PriceRangeName)
class PriceRangeNameAdmin(admin.ModelAdmin):
    list_display = ['__str__']


@admin.register(models.PossibleRangePrices)
class PossibleRangePricesAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'bank', 'law', 'guarantee', "have_advance", 'date_range_name', 'price_range_name']
    list_editable = ['bank', 'law', 'guarantee', "have_advance", 'date_range_name', 'price_range_name']


# Добавил новое
class BaseBanksPricesAdminForm(forms.ModelForm):
    class Meta:
        model = models.BaseBanksPrices
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Обработка possible_range_prices для фильтрации date_range и price_range
        if 'possible_range_prices' in self.data:
            try:
                possible_range_prices_id = int(self.data.get('possible_range_prices'))
                possible_range = models.PossibleRangePrices.objects.get(id=possible_range_prices_id)

                # Фильтрация для date_range
                date_range_name = possible_range.date_range_name
                if date_range_name:
                    self.fields['date_range'].queryset = models.DateRange.objects.filter(
                        date_range_name=date_range_name)
                else:
                    self.fields['date_range'].queryset = models.DateRange.objects.none()

                # Фильтрация для price_range
                price_range_name = possible_range.price_range_name
                if price_range_name:
                    self.fields['price_range'].queryset = models.PriceRange.objects.filter(
                        price_range_name=price_range_name)
                else:
                    self.fields['price_range'].queryset = models.PriceRange.objects.none()

            except (ValueError, TypeError, models.PossibleRangePrices.DoesNotExist):
                self.fields['date_range'].queryset = models.DateRange.objects.none()
                self.fields['price_range'].queryset = models.PriceRange.objects.none()
        elif self.instance.pk and self.instance.possible_range_prices:
            # Для редактирования существующего объекта
            possible_range = self.instance.possible_range_prices

            # Фильтрация для date_range
            date_range_name = possible_range.date_range_name
            if date_range_name:
                self.fields['date_range'].queryset = models.DateRange.objects.filter(date_range_name=date_range_name)
            else:
                self.fields['date_range'].queryset = models.DateRange.objects.none()

            # Фильтрация для price_range
            price_range_name = possible_range.price_range_name
            if price_range_name:
                self.fields['price_range'].queryset = models.PriceRange.objects.filter(
                    price_range_name=price_range_name)
            else:
                self.fields['price_range'].queryset = models.PriceRange.objects.none()
        else:
            # При первой загрузке формы создания
            self.fields['date_range'].queryset = models.DateRange.objects.none()
            self.fields['price_range'].queryset = models.PriceRange.objects.none()


@admin.register(models.BaseBanksPrices)
class BaseBanksPricesAdmin(admin.ModelAdmin):
    form = BaseBanksPricesAdminForm
    list_display = ["possible_range_prices", "price_range", "date_range", "year_percent"]
    list_editable = ["price_range", "date_range", "year_percent"]


@admin.register(models.MinBanksPrices)
class MinBanksPricesAdmin(admin.ModelAdmin):
    list_display = ["possible_range_prices", "price_range", "date_range", "min_value"]
    list_editable = ["price_range", "date_range", "min_value"]
