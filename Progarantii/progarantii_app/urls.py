from django.urls import path
from . import views

urlpatterns = [
    path("", views.MenuView.as_view(), name='menu'),
    path("create-percent/", views.BaseBanksPricesView.as_view(), name='basebanksprices'),
    path('create-object/', views.PossibleRangePricesView.as_view(), name='possiblerangeprices')
]
