from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import PossibleRangePrices, PriceRange, DateRange, BaseBanksPrices


class BaseBanksPricesView(LoginRequiredMixin, View):
    def get(self, request):
        possible_range_prices_list = PossibleRangePrices.objects.all()
        return render(request, "progarantii_app/table.html", {"possible_range_prices_list": possible_range_prices_list})

    def post(self, request):
        possible_range_prices_id = request.POST.get("possible_range_prices_id")
        if not possible_range_prices_id:
            return render(request, "progarantii_app/table.html", {
                "possible_range_prices_list": PossibleRangePrices.objects.all(),
                "error": "Выберите PossibleRangePrices!"
            })

        possible_range_prices = get_object_or_404(PossibleRangePrices, id=possible_range_prices_id)

        # Сохранение данных
        for key, value in request.POST.items():
            if key.startswith("year_percent_"):
                parts = key.split("_")
                if len(parts) == 4:  # Ожидаем ["year", "percent", date_id, price_id]
                    date_id = parts[2]
                    price_id = parts[3]
                    base_banks_price, _ = BaseBanksPrices.objects.get_or_create(
                        possible_range_prices=possible_range_prices,
                        price_range_id=price_id,
                        date_range_id=date_id,
                        defaults={"year_percent": None}
                    )
                    base_banks_price.year_percent = value if value else None
                    base_banks_price.save()

        price_ranges = PriceRange.objects.filter(price_range_name=possible_range_prices.price_range_name)
        date_ranges = DateRange.objects.filter(date_range_name=possible_range_prices.date_range_name)

        # Подготовка данных для матрицы
        table_data = {}
        for date_range in date_ranges:
            table_data[date_range.id] = {}
            for price_range in price_ranges:
                base_banks_price, _ = BaseBanksPrices.objects.get_or_create(
                    possible_range_prices=possible_range_prices,
                    price_range=price_range,
                    date_range=date_range,
                    defaults={"year_percent": None}
                )
                table_data[date_range.id][price_range.id] = base_banks_price.year_percent or ''

        return render(request, "progarantii_app/table.html", {
            "possible_range_prices_list": PossibleRangePrices.objects.all(),
            "selected_possible_range_prices": possible_range_prices,
            "price_ranges": price_ranges,
            "date_ranges": date_ranges,
            "table_data": table_data,
            "success": "Данные успешно сохранены!"
        })
