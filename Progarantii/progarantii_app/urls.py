from django.urls import path
from .views import BaseBanksPricesView

urlpatterns = [
    path("", BaseBanksPricesView.as_view(), name='basebanksprices'),
]