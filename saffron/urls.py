from django.urls import path
from saffron.views import *


app_name = 'saffron'

urlpatterns = [
    path('', index, name='index'),
    path('add/cash_transfer/<str:cash_transfer_type>', add_cash_transfer, name='add_cash_transfer'),
    path('add/category', add_category, name='add_category'),
    path('add/trade', add_trade, name='add_trade'),
    path('inquery/balance', inquery_balance, name='inquery_balance'),
    path('inquery/<str:trade_type>', inquery_trades, name='inquery_trades'),
    path('inquery/payments/<int:trade_id>', inquery_trade_payments, name='inquery_trade_payments'),
]
