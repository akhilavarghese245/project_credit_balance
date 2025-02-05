from django.contrib import admin
from django.urls import path
from .views import BillView, BillPayment

urlpatterns = [
    path('api/pay_bill/', BillView.as_view(), name='pay_bill'),
    path('api/pay/', BillPayment.as_view(), name='pay'),

]
