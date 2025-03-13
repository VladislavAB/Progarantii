from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from . import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class BankGuaranteeAPIView(APIView):
    def get(self, request):
        advance_choices = {'y': True, 'n': False}
        guarantee_choices = {'i': 'Исполнение', 'u': 'Участие', 'g': 'Гарантийные обязательства'}
        law_choices = {44: "№ 44", 223: "№ 223", 615: "№ 615"}
        year_percent = 0.0
        min_value = 0.0

        # Просим:
        # bank=SBER&s=23423423,0&d=234&t=44&a=n&m=i
        # bank - идентификатор банка +++
        # s - сумма
        # d - кол-во дней
        # t - закон [44,223,615] +++
        # a - наличие аванса [y,n] +++
        # m - тип гарантии [i,u,g] +++

        # Получаем:
        # {id": "derzhava",
        #     "name": "Держава",
        #     «Expert_RA»: "BBB-(RU)»,
        #   «AKRA_rating»: "BBB-(RU)»,
        #     «base_percent»: 3,
        #     «min_price»: 34}
        # Пример: http://127.0.0.1:8000/api/?bank=alpha&s=60000&d=60&t=223&a=n&m=u

        # Вытаскиваю из request все параметры, которые были переданы в поисковую строку
        bank_short = request.query_params.get('bank').lower()
        law_number = law_choices[int(request.query_params.get('t'))]
        guarantee = guarantee_choices[request.query_params.get('m')]
        have_advance = advance_choices[request.query_params.get('a')]
        number_of_days = int(request.query_params.get('d'))
        price = int(request.query_params.get('s'))
        bank_obj = models.Bank.objects.get(short_name=bank_short)

        # Ищу по параметрам объект, он может быть единственным уникальным с 4 одинаковыми параметрами.
        possible_range_price = models.PossibleRangePrices.objects.filter(bank__short_name=bank_short,
                                                                         law__type_of_law=law_number,
                                                                         guarantee__type_of_guarantee=guarantee,
                                                                         have_advance=have_advance).first()
        # Ищу все объекты с possible_range_prices
        all_base_bank_percents = models.BaseBankPercent.objects.filter(possible_range_prices=possible_range_price)

        # Ищу пересечения
        for base_bank_percent in all_base_bank_percents:
            base_price_range_start, base_price_range_end = (base_bank_percent.price_range.start_price,
                                                            base_bank_percent.price_range.end_price)
            base_date_range_start, base_date_range_end = (base_bank_percent.date_range.start_date,
                                                          base_bank_percent.date_range.end_date)
            if number_of_days in range(base_date_range_start, base_date_range_end + 1) and price in range(
                    base_price_range_start, base_price_range_end + 1):
                year_percent = base_bank_percent.year_percent
                break

        # Ищу все объекты с possible_range_prices
        all_min_bank_prices = models.MinBankPrice.objects.filter(possible_range_prices=possible_range_price)

        # Ищу пересечения
        for min_bank_price in all_min_bank_prices:
            price_range_start, price_range_end = (min_bank_price.price_range.start_price,
                                                  min_bank_price.price_range.end_price)
            date_range_start, date_range_end = (min_bank_price.date_range.start_date,
                                                min_bank_price.date_range.end_date)
            if number_of_days in range(date_range_start, date_range_end + 1) and price in range(price_range_start,
                                                                                                price_range_end + 1):
                min_value = min_bank_price.min_value
                break

        # Формирую ответ
        data = {'id': bank_obj.short_name, 'name': bank_obj.full_name, 'AKRA_rating': bank_obj.AKRA_rating,
                'Expert_RA': bank_obj.Expert_RA, 'base_percent': year_percent, 'min_price': min_value}
        return Response(data, status=status.HTTP_200_OK)


class MenuView(LoginRequiredMixin, TemplateView):
    template_name = 'progarantii_app/menu.html'


class PossibleRangePricesView(LoginRequiredMixin, View):
    def get(self, request):
        banks = models.Bank.objects.all()
        laws = models.Law.objects.all()
        guarantees = models.Guarantee.objects.all()
        date_range_names = models.DateRangeName.objects.all()
        price_range_names = models.PriceRangeName.objects.all()
        existing_objects = models.PossibleRangePrices.objects.all()

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
        # Обработка удаления
        if 'delete_id' in request.POST:
            delete_id = request.POST.get('delete_id')
            obj = get_object_or_404(models.PossibleRangePrices, id=delete_id)
            obj.delete()
            return redirect('possiblerangeprices')

        # Получаем данные из формы
        bank_id = request.POST.get('bank')
        law_id = request.POST.get('law')
        guarantee_id = request.POST.get('guarantee')
        date_range_name_id = request.POST.get('date_range_name')
        price_range_name_id = request.POST.get('price_range_name')
        have_advance = request.POST.get('have_advance') == 'on'

        # Преобразуем пустые строки в None для корректной проверки
        bank = models.Bank.objects.get(id=bank_id) if bank_id else None
        law = models.Law.objects.get(id=law_id) if law_id else None
        guarantee = models.Guarantee.objects.get(id=guarantee_id) if guarantee_id else None

        # Проверка на дубликат
        duplicate_exists = models.PossibleRangePrices.objects.filter(
            bank=bank,
            law=law,
            guarantee=guarantee,
            have_advance=have_advance
        ).exists()

        if duplicate_exists:
            # Если дубликат найден, возвращаем страницу с ошибкой
            banks = models.Bank.objects.all()
            laws = models.Law.objects.all()
            guarantees = models.Guarantee.objects.all()
            date_range_names = models.DateRangeName.objects.all()
            price_range_names = models.PriceRangeName.objects.all()
            existing_objects = models.PossibleRangePrices.objects.all()

            context = {
                'banks': banks,
                'laws': laws,
                'guarantees': guarantees,
                'date_range_names': date_range_names,
                'price_range_names': price_range_names,
                'existing_objects': existing_objects,
                'error': 'Объект с таким сочетанием банка, закона, типа обеспечения и аванса уже существует!'
            }
            return render(request, 'progarantii_app/create_object.html', context)

        # Если дубликата нет, создаём объект
        possible_range_price = models.PossibleRangePrices(
            bank=bank,
            law=law,
            guarantee=guarantee,
            date_range_name=models.DateRangeName.objects.get(id=date_range_name_id) if date_range_name_id else None,
            price_range_name=models.PriceRangeName.objects.get(id=price_range_name_id) if price_range_name_id else None,
            have_advance=have_advance
        )
        possible_range_price.save()

        # Возвращаем страницу с сообщением об успехе
        return redirect('possiblerangeprices')


class BaseBankPercentView(LoginRequiredMixin, View):
    def get(self, request):
        possible_range_prices_list = models.PossibleRangePrices.objects.all()
        return render(request, "progarantii_app/create_percent.html", {
            "possible_range_prices_list": possible_range_prices_list
        })

    def post(self, request):
        possible_range_prices_id = request.POST.get("possible_range_prices_id")
        if not possible_range_prices_id:
            return render(request, "progarantii_app/create_percent.html", {
                "possible_range_prices_list": models.PossibleRangePrices.objects.all(),
                "error": "Выберите PossibleRangePrices!"
            })

        possible_range_prices = get_object_or_404(models.PossibleRangePrices, id=possible_range_prices_id)

        # Сохранение данных для обеих таблиц
        for key, value in request.POST.items():
            if key.startswith("year_percent_"):
                parts = key.split("_")
                if len(parts) == 4:  # ["year", "percent", date_id, price_id]
                    date_id = parts[2]
                    price_id = parts[3]
                    base_banks_price, _ = models.BaseBankPercent.objects.get_or_create(
                        possible_range_prices=possible_range_prices,
                        price_range_id=price_id,
                        date_range_id=date_id,
                        defaults={"year_percent": None}
                    )
                    base_banks_price.year_percent = value if value else None
                    base_banks_price.save()

            elif key.startswith("min_value_"):
                parts = key.split("_")
                if len(parts) == 4:  # ["min", "value", date_id, price_id]
                    date_id = parts[2]
                    price_id = parts[3]
                    min_banks_price, _ = models.MinBankPrice.objects.get_or_create(
                        possible_range_prices=possible_range_prices,
                        price_range_id=price_id,
                        date_range_id=date_id,
                        defaults={"min_value": None}
                    )
                    min_banks_price.min_value = value if value else None
                    min_banks_price.save()
                    print(f"Saved MinBanksPrices: date_id={date_id}, price_id={price_id}, min_value={value}")

        # Получение связанных диапазонов
        price_ranges = models.PriceRange.objects.filter(price_range_name=possible_range_prices.price_range_name)
        date_ranges = models.DateRange.objects.filter(date_range_name=possible_range_prices.date_range_name)

        # Данные для BaseBanksPrices
        base_table_data = {}
        for date_range in date_ranges:
            base_table_data[date_range.id] = {}
            for price_range in price_ranges:
                base_banks_price, _ = models.BaseBankPercent.objects.get_or_create(
                    possible_range_prices=possible_range_prices,
                    price_range=price_range,
                    date_range=date_range,
                    defaults={"year_percent": None}
                )
                base_table_data[date_range.id][price_range.id] = base_banks_price.year_percent or ''

        # Данные для MinBanksPrices
        min_table_data = {}
        for date_range in date_ranges:
            min_table_data[date_range.id] = {}
            for price_range in price_ranges:
                min_banks_price, _ = models.MinBankPrice.objects.get_or_create(
                    possible_range_prices=possible_range_prices,
                    price_range=price_range,
                    date_range=date_range,
                    defaults={"min_value": None}
                )
                min_table_data[date_range.id][price_range.id] = min_banks_price.min_value or ''

        return render(request, "progarantii_app/create_percent.html", {
            "possible_range_prices_list": models.PossibleRangePrices.objects.all(),
            "selected_possible_range_prices": possible_range_prices,
            "price_ranges": price_ranges,
            "date_ranges": date_ranges,
            "base_table_data": base_table_data,
            "min_table_data": min_table_data,
            "success": "Данные успешно сохранены!"
        })
