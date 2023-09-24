import jdatetime
from django.db import models
from django.forms import ModelForm


class Saffron(models.Model):
    is_buy = models.BooleanField()
    saffron_type = models.ForeignKey('SaffronCategory', on_delete=models.CASCADE)
    gram_price = models.IntegerField()  # Price of saffron 1 gram on that moment
    weight_gram = models.FloatField()
    all_amount_tmn = models.IntegerField()
    description = models.TextField()
    payments = models.ManyToManyField('Payment')
    datetime = models.DateTimeField()

    def __str__(self):
        _type = 'خرید' if self.is_buy else 'فروش'
        return '{} {} گرم / {} تومان'.format(_type, self.weight_gram, self.gram_price)


class SaffronCategory(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category


class Payment(models.Model):
    amount = models.IntegerField()
    datetime = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return '{} تومان - {}'.format(self.amount, self.datetime.strftime('%Y/%m/%d'))