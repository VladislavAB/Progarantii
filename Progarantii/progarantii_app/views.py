from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from . import models


class MenuView(LoginRequiredMixin, TemplateView):
    template_name = 'progarantii_app/menu.html'


class PossibleRangePricesView(LoginRequiredMixin, View):
    def get(self, request):
        # Получаем данные для выпадающих списков
        banks = models.Bank.objects.all()
        laws = models.Law.objects.all()
        guarantees = models.Guarantee.objects.all()
        date_range_names = models.DateRangeName.objects.all()
        price_range_names = models.PriceRangeName.objects.all()

        # Получаем все существующие объекты PossibleRangePrices
        existing_objects = models.PossibleRangePrices.objects.all()

        # Передаем данные в шаблон
        context = {
            'banks': banks,
            'laws': laws,
            'guarantees': guarantees,
            'date_range_names': date_range_names,
            'price_range_names': price_range_names,
            'existing_objects': existing_objects,
        }
        return render(request, 'progarantii_app/create_object.html', context)

    def post(self, request):
        # Получаем данные из формы
        bank_id = request.POST.get('bank')
        law_id = request.POST.get('law')
        guarantee_id = request.POST.get('guarantee')
        date_range_name_id = request.POST.get('date_range_name')
        price_range_name_id = request.POST.get('price_range_name')
        have_advance = request.POST.get('have_advance') == 'on'  # Checkbox возвращает 'on' или None

        # Создаем новый объект
        possible_range_price = models.PossibleRangePrices(
            bank=models.Bank.objects.get(id=bank_id) if bank_id else None,
            law=models.Law.objects.get(id=law_id) if law_id else None,
            guarantee=models.Guarantee.objects.get(id=guarantee_id) if guarantee_id else None,
            date_range_name=models.DateRangeName.objects.get(id=date_range_name_id) if date_range_name_id else None,
            price_range_name=models.PriceRangeName.objects.get(id=price_range_name_id) if price_range_name_id else None,
            have_advance=have_advance
        )
        possible_range_price.save()

        # Перенаправляем на ту же страницу после сохранения
        return redirect('possiblerangeprices')


class BaseBanksPricesView(LoginRequiredMixin, View):
    def get(self, request):
        possible_range_prices_list = models.PossibleRangePrices.objects.all()
        return render(request, "progarantii_app/create_percent.html", {"possible_range_prices_list": possible_range_prices_list})

    def post(self, request):
        possible_range_prices_id = request.POST.get("possible_range_prices_id")
        if not possible_range_prices_id:
            return render(request, "progarantii_app/create_percent.html", {
                "possible_range_prices_list": models.PossibleRangePrices.objects.all(),
                "error": "Выберите PossibleRangePrices!"
            })

        possible_range_prices = get_object_or_404(models.PossibleRangePrices, id=possible_range_prices_id)

        # Сохранение данных
        for key, value in request.POST.items():
            if key.startswith("year_percent_"):
                parts = key.split("_")
                if len(parts) == 4:  # Ожидаем ["year", "percent", date_id, price_id]
                    date_id = parts[2]
                    price_id = parts[3]
                    base_banks_price, _ = models.BaseBanksPrices.objects.get_or_create(
                        possible_range_prices=possible_range_prices,
                        price_range_id=price_id,
                        date_range_id=date_id,
                        defaults={"year_percent": None}
                    )
                    base_banks_price.year_percent = value if value else None
                    base_banks_price.save()

        price_ranges = models.PriceRange.objects.filter(price_range_name=possible_range_prices.price_range_name)
        date_ranges = models.DateRange.objects.filter(date_range_name=possible_range_prices.date_range_name)

        # Подготовка данных для матрицы
        table_data = {}
        for date_range in date_ranges:
            table_data[date_range.id] = {}
            for price_range in price_ranges:
                base_banks_price, _ = models.BaseBanksPrices.objects.get_or_create(
                    possible_range_prices=possible_range_prices,
                    price_range=price_range,
                    date_range=date_range,
                    defaults={"year_percent": None}
                )
                table_data[date_range.id][price_range.id] = base_banks_price.year_percent or ''

        return render(request, "progarantii_app/create_percent.html", {
            "possible_range_prices_list": models.PossibleRangePrices.objects.all(),
            "selected_possible_range_prices": possible_range_prices,
            "price_ranges": price_ranges,
            "date_ranges": date_ranges,
            "table_data": table_data,
            "success": "Данные успешно сохранены!"
        })
