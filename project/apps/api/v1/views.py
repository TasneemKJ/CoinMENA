import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RateSerializer
from .models import Rate
from .services import Alphaavantage

from django.core.cache import cache

logger = logging.Logger(__name__)


class RateViews(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get latest price of BTC/USD"""
        try:
            rate = cache.get("latest_rate")
            if rate:
                serializer = RateSerializer(rate)
                return Response({"status": "success", "data": serializer.data, "message": ""},
                                status=status.HTTP_200_OK)
            try:
                rate = Rate.objects.latest('id')
            except:
                rate = None

            if rate:
                cache.set("latest_rate", rate, timeout=60 * 60)
                serializer = RateSerializer(rate)
                return Response({"status": "success", "data": serializer.data, "message": ""},
                                status=status.HTTP_200_OK)
            else:
                return Response(
                    {"status": "success", "data": None, "message": "No exchange rate available!"},
                    status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({"status": "error", "data": None, "message": "Cannot get exchange rate. please try again!"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Force update price of BTC/USD from the alphavantage API"""
        try:
            data = Alphaavantage.call_alphaavantage_api()
            if data:
                exchange_rate, pid_price, ask_price = Alphaavantage.extract_alphaavantage_api_data(data)
                if exchange_rate is not None and pid_price is not None and ask_price is not None:
                    rate = Rate.objects.create(code="USD", exchange_rate=exchange_rate, pid_price=pid_price,
                                               ask_price=ask_price)
                    cache.set("latest_rate", rate, timeout=60 * 60)
                    serializer = RateSerializer(rate)
                    return Response({"status": "success", "data": serializer.data, "message": ""},
                                    status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"status": "error", "data": None, "message": "Cannot get exchange rate. please try again!"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(
                    {"status": "error", "data": None, "message": "Cannot get exchange rate. please try again!"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(e)
            return Response({"status": "error", "data": None, "message": "Cannot get exchange rate. please try again!"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
