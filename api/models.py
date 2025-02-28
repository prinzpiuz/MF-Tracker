from django.db import models
from django.contrib.auth.models import User


class DateMixin(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MutualFund(DateMixin):
    name = models.CharField(max_length=100)
    scheme_Code = models.CharField(max_length=100, unique=True)
    nav = models.DecimalField(max_digits=10, decimal_places=2)


class UserFunds(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mutual_fund = models.ForeignKey(MutualFund, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
