from django.db import models

# Create your models here.
class Orders(models.Model):
    time = models.CharField(max_length=30)
    name_cript = models.CharField(verbose_name="Название крипты", max_length=15)
    price_buy = models.FloatField(verbose_name="Цена покупки")
    price_in_1hour = models.FloatField(verbose_name="Цена за час", null=True)
    price_in_2hour = models.FloatField(verbose_name="Цена за 2 часа", null=True)
    price_in_3hour = models.FloatField(verbose_name="Цена за 3 часа", null=True)
    price_in_5hour = models.FloatField(verbose_name="Цена за 5 часов", null=True)
    price_in_24hour = models.FloatField(verbose_name="Цена за сутки", null=True)


    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Данные ордеров'

    def __str__(self):
        return self.name_cript
