from django.db import models


class Rate(models.Model):
    code = models.CharField(max_length=3)

    exchange_rate = models.FloatField()
    pid_price = models.FloatField()
    ask_price = models.FloatField()

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}:{}".format(self.code, self.exchange_rate)
