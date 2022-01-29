from celery import shared_task
from celery.utils.log import get_task_logger

from apps.api.v1.models import Rate
from apps.api.v1.services import Alphaavantage

from django.core.cache import cache

logger = get_task_logger(__name__)


@shared_task
def update_rates_task():
    """Fetches the price of BTC/USD from the alphavantage API every hour"""
    logger.info("update_rates_task: Started.")

    try:
        data = Alphaavantage.call_alphaavantage_api()
        logger.info("update_rates_task: {}".format(data))
        if data:
            exchange_rate, pid_price, ask_price = Alphaavantage.extract_alphaavantage_api_data(data)
            if exchange_rate is not None and pid_price is not None and ask_price is not None:
                rate = Rate.objects.create(code="USD", exchange_rate=exchange_rate, pid_price=pid_price,
                                           ask_price=ask_price)
                if rate:
                    cache.set("latest_rate", rate, timeout=60 * 60)
                    logger.info("update_rates_task: Added rate.")
                    logger.info("update_rates_task: {}".format(rate))
                else:
                    logger.error("update_rates_task: Failed - Rates not added")
            else:
                logger.info("update_rates_task: Failed - No rate.")
        else:
            logger.info("update_rates_task: Failed - No data")
    except Exception as e:
        logger.error("update_rates_task: Failed - {}".format(e))
