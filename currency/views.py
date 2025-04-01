from django.shortcuts import render
from .forms import CurrencyConverterForm
from .models import ExchangeRate
from decimal import Decimal

def currency_converter(request):
    result = None
    form = CurrencyConverterForm(request.POST or None)
    
    # Fixed exchange rates (update these manually when needed)
    EXCHANGE_RATES = {
        'USD_KHR': Decimal('4100.00'),  # 1 USD = 4100 KHR
        'KHR_USD': Decimal('0.00024'),  # 1 KHR = 0.00024 USD
    }

    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']
        from_currency = form.cleaned_data['from_currency']
        to_currency = form.cleaned_data['to_currency']

        if from_currency == 'USD' and to_currency == 'KHR':
            result = amount * EXCHANGE_RATES['USD_KHR']
        elif from_currency == 'KHR' and to_currency == 'USD':
            result = amount * EXCHANGE_RATES['KHR_USD']
        else:
            result = amount

    return render(request, 'currency/converter.html', {
        'form': form,
        'result': result,
        'usd_rate': EXCHANGE_RATES['USD_KHR'],
        'khr_rate': EXCHANGE_RATES['KHR_USD'],
    })