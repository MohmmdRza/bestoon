import json
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from saffron.models import *
import datetime as dt
import jdatetime as jdt


@login_required
def index(request):
    return render(request, 'saffron/index.html')


@login_required
def add_cash_transfer(request, cash_transfer_type):
    context = {}
    saffron_trades = Saffron.objects.filter(is_buy=cash_transfer_type == 'payment')
    context['ok'] = False
    context['cash_transfer_type'] = cash_transfer_type
    context['saffron_trades'] = saffron_trades
    if request.method == 'POST':
        context['data'] = request.POST

        datetime = request.POST.get('datetime') or ""
        datetime_validation = True
        try:
            datetime = jdt.datetime.strptime(datetime, "%Y/%m/%d")
            datetime_validation = bool(datetime)
        except ValueError:
            datetime_validation = False
        if not datetime_validation:
            context['message'] = 'تاریخ درست وارد نشده است !'
            return render(request, 'saffron/add_cash_transfer.html', context)
        datetime = dt.datetime.fromtimestamp(datetime.timestamp())

        amount = request.POST.get('amount') or ""
        if not amount.isdigit():
            context['message'] = 'مبلغ فقط عدد  می تواند باشد !'
            return render(request, 'saffron/add_cash_transfer.html', context)
        amount = int(amount)

        trade_pk = request.POST.get('trade') or -1
        trade_query = Saffron.objects.filter(pk=trade_pk)
        if len(trade_query) == 0:
            context['message'] = 'مشکلی در شناسایی معامله پیش آمد !'
            return render(request, 'saffron/add_cash_transfer.html', context)

        new_payment = Payment.objects.create(
            amount=amount,
            description=request.POST.get('description') or "",
            datetime=datetime,
        )
        new_payment.save()

        trade = trade_query[0]
        trade.payments.add(new_payment)
        trade.save()

        context['ok'] = True
        context['message'] = 'با موفقیت اضافه شد !'
        return render(request, 'saffron/add_cash_transfer.html', context)
    else:
        now = jdt.datetime.now().strftime('%Y/%m/%d')
        data = {'today': now}
        context['data'] = data
        return render(request, 'saffron/add_cash_transfer.html', context)


@login_required
def add_category(request):
    if request.method == 'POST':
        category = request.POST['saffron_type']
        category_exists = len(SaffronCategory.objects.filter(category=category)) > 0

        context = {}
        context['ok'] = False
        context['data'] = request.POST
        if category_exists:
            context['message'] = 'از قبل موجود بود !'
            return render(request, 'saffron/add_category_form.html', context)
        new_category = SaffronCategory.objects.create(category=category)
        new_category.save()

        context['ok'] = True
        context['message'] = 'با موفقیت اضافه شد !'

        return render(request, 'saffron/add_category_form.html', context)
    else:
        return render(request, 'saffron/add_category_form.html')


@login_required
def add_trade(request):
    if request.method == 'POST':
        trade_type = request.POST.get('trade_type')
        gram_price = request.POST.get('price')
        weight_gram = request.POST.get('weight')
        all_amount = request.POST.get('all_amount')
        datetime = request.POST.get('datetime')
        description = request.POST.get('description') or ""

        context = {}

        saffron_categories = SaffronCategory.objects.all()
        context['saffron_categories'] = saffron_categories

        context['data'] = request.POST
        context['ok'] = False

        datetime_validation = True
        try:
            datetime = jdt.datetime.strptime(datetime, "%Y/%m/%d")
            datetime_validation = bool(datetime)
        except ValueError as e:
            datetime_validation = False
        if not datetime_validation:
            context['message'] = 'تاریخ درست وارد نشده است ! '
            return render(request, 'saffron/add_trade_form.html', context)
        if gram_price is None or not gram_price.isdigit():
            context['message'] = 'قیمت هر گرم درست وارد نشده است !'
            return render(request, 'saffron/add_trade_form.html', context)
        if weight_gram is None or not weight_gram.replace('.', '').isdigit():
            context['message'] = 'وزن نمی تواند خالی باشد !'
            return render(request, 'saffron/add_trade_form.html', context)
        if all_amount is None or not all_amount.isdigit():
            context['message'] = 'هزینه ی نهایی نمی تواند خالی باشد !'
            return render(request, 'saffron/add_trade_form.html', context)

        datetime = dt.datetime.fromtimestamp(datetime.timestamp())
        saffron_category = saffron_categories.filter(category=request.POST['saffron_category'])[0]
        Saffron.objects.create(
            is_buy=trade_type == 'buy',
            saffron_type=saffron_category,
            gram_price=int(gram_price),
            weight_gram=float(weight_gram),
            all_amount_tmn=int(all_amount),
            datetime=datetime,
            description=description
        )
        context['ok'] = True
        context['message'] = 'با موفقیت ثبت شد !'
        return render(request, 'saffron/add_trade_form.html', context)
    else:
        saffron_categories = SaffronCategory.objects.all()
        now = jdt.datetime.now().strftime('%Y/%m/%d')
        return render(request, 'saffron/add_trade_form.html', {
            'saffron_categories': saffron_categories,
            'data': {
                'today': now
            }
        })


@login_required
def inquery_balance(request):
    saffron_categories = SaffronCategory.objects.all()
    trades = Saffron.objects.all()
    context = {}
    result = {}
    for cat in saffron_categories:
        if len(cat.__str__()) == 0: continue
        buy_weight_sum = trades.filter(saffron_type=cat, is_buy=True) \
            .aggregate(Sum('weight_gram'))['weight_gram__sum'] or 0
        sell_weight_sum = trades.filter(saffron_type=cat, is_buy=False)\
            .aggregate(Sum('weight_gram'))['weight_gram__sum'] or 0
        balance = buy_weight_sum - sell_weight_sum
        balance = balance if int(balance) != float(balance) else int(balance)
        # if balance < 0: balance = 'منفی {}'.format(balance * -1)
        result[cat.__str__()] = balance
    context['result'] = result
    return render(request, 'saffron/inquery_balance.html', context)


@login_required
def inquery_trades(request, trade_type):
    trades = Saffron.objects.filter(is_buy=trade_type == 'buys')
    result = []
    return render(request, 'saffron/inquery_trades.html', context={
        'trade_type': trade_type,
        'trades': trades
    })


@login_required
def inquery_trade_payments(request, trade_id):
    print(trade_id)
    trade = Saffron.objects.filter(pk=trade_id)[0]
    payments = trade.payments.all()

    all_amount = trade.all_amount_tmn
    paid_amount = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    remains_amount = all_amount - paid_amount

    return render(request, 'saffron/inquery_cash_transfers.html', context={
        'payments': payments,
        'all_amount': all_amount,
        'paid_amount': paid_amount,
        'remains_amount': remains_amount
    })