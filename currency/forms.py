from django import forms

CURRENCY_CHOICES = [
    ('KHR', 'Cambodian Riel'),
    ('USD', 'US Dollar'),
]

class CurrencyConverterForm(forms.Form):
    amount = forms.DecimalField(
        label='Amount',
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount'
        })
    )
    from_currency = forms.ChoiceField(
        label='From',
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    to_currency = forms.ChoiceField(
        label='To',
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )