import requests

from core import settings


class Alphaavantage:
    """Handle the alphavantage API"""

    @staticmethod
    def call_alphaavantage_api(to_currency='USD'):
        """Call the alphavantage API"""
        url = '{}/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency={}&apikey={}'.format(
            settings.ALPHAVANTAGE_BASE_URL, to_currency, settings.ALPHAVANTAGE_API_KEY)
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
        else:
            data = None
        return data

    @staticmethod
    def extract_alphaavantage_api_data(data):
        """Extract data from the alphavantage API Response"""
        if data:
            data = data.get("Realtime Currency Exchange Rate", {})
            exchange_rate = data.get("5. Exchange Rate", None)
            pid_price = data.get("8. Bid Price", None)
            ask_price = data.get("9. Ask Price", None)
            return exchange_rate, pid_price, ask_price
        else:
            return None, None, None
