from django.core.management.base import BaseCommand
from currency.models import ExchangeRate
from decimal import Decimal
import requests

class Command(BaseCommand):
    help = 'Update currency exchange rates'

    def handle(self, *args, **options):
        # Using free API from Frankfurter.app
        try:
            response = requests.get('https://api.frankfurter.app/latest?from=USD&to=KHR')
            data = response.json()
            
            if 'rates' in data and 'KHR' in data['rates']:
                usd_to_khr_rate = Decimal(str(data['rates']['KHR']))
                
                ExchangeRate.objects.update_or_create(
                    currency_from='USD',
                    currency_to='KHR',
                    defaults={'rate': usd_to_khr_rate}
                )
                
                ExchangeRate.objects.update_or_create(
                    currency_from='KHR',
                    currency_to='USD',
                    defaults={'rate': Decimal(1)/usd_to_khr_rate}
                )
                
                self.stdout.write(self.style.SUCCESS(f'Successfully updated rates: 1 USD = {usd_to_khr_rate} KHR'))
            else:
                self.stdout.write(self.style.WARNING('API response missing expected data. Using fallback rates.'))
                self.set_fallback_rates()
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating rates: {e}. Using fallback rates.'))
            self.set_fallback_rates()

    def set_fallback_rates(self):
        """Set reasonable default rates if API fails"""
        ExchangeRate.objects.update_or_create(
            currency_from='USD',
            currency_to='KHR',
            defaults={'rate': Decimal('4100.00')}
        )
        
        ExchangeRate.objects.update_or_create(
            currency_from='KHR',
            currency_to='USD',
            defaults={'rate': Decimal('0.00024')}
        )