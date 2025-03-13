from rest_framework import serializers
from . import models


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = ['id', 'full_name', 'short_name', 'license_number', 'url', 'AKRA_rating', 'Expert_RA']


class LawSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Law
        fields = ['id', 'type_of_law']


class GuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guarantee
        fields = ['id', 'type_of_guarantee']


class DateRangeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DateRangeName
        fields = ['id', 'name']


class DateRangeSerializer(serializers.ModelSerializer):
    date_range_name = DateRangeNameSerializer()

    class Meta:
        model = models.DateRange
        fields = ['id', 'start_date', 'end_date', 'date_range_name']


class PriceRangeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PriceRangeName
        fields = ['id', 'name']


class PriceRangeSerializer(serializers.ModelSerializer):
    price_range_name = PriceRangeNameSerializer()

    class Meta:
        model = models.PriceRange
        fields = ['id', 'start_price', 'end_price', 'price_range_name']


class PossibleRangePricesSerializer(serializers.ModelSerializer):
    bank = BankSerializer()
    law = LawSerializer()
    guarantee = GuaranteeSerializer()
    date_range_name = DateRangeNameSerializer()
    price_range_name = PriceRangeNameSerializer()

    class Meta:
        model = models.PossibleRangePrices
        fields = ['id', 'bank', 'law', 'guarantee', 'have_advance', 'date_range_name', 'price_range_name']


class BaseBankPercentSerializer(serializers.ModelSerializer):
    possible_range_prices = PossibleRangePricesSerializer()
    price_range = PriceRangeSerializer()
    date_range = DateRangeSerializer()

    class Meta:
        model = models.BaseBankPercent
        fields = ['id', 'possible_range_prices', 'price_range', 'date_range', 'year_percent']


class MinBankPriceSerializer(serializers.ModelSerializer):
    possible_range_prices = PossibleRangePricesSerializer()
    price_range = PriceRangeSerializer()
    date_range = DateRangeSerializer()

    class Meta:
        model = models.MinBankPrice
        fields = ['id', 'possible_range_prices', 'price_range', 'date_range', 'min_value']
