from django.urls import path
from . import views

urlpatterns = [
    path("", views.MenuView.as_view(), name='menu'),
    path("create-percent/", views.BaseBankPercentView.as_view(), name='basebanksprices'),
    path('create-object/', views.PossibleRangePricesView.as_view(), name='possiblerangeprices'),
    path('api/', views.BankGuaranteeAPIView.as_view())

]
