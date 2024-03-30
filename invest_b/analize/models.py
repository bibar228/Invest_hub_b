from django.db import models

# Create your models here.
class Orders(models.Model):
    time = models.CharField(max_length=30)
    chat_title = models.CharField(verbose_name="Название чата", max_length=100, null=True)
    name_cript = models.CharField(verbose_name="Название крипты", max_length=15)
    price_buy = models.FloatField(verbose_name="Цена покупки")
    description = models.CharField(verbose_name="Действие", max_length=15, null=True)
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

class Siggs(models.Model):
    cryptocode = models.CharField(max_length=30)
    init_time = models.CharField(max_length=30)
    end_time = models.CharField(max_length=30)
    trade_position = models.CharField(verbose_name="LONG/SHORT", max_length=15)
    trade_position_start = models.FloatField(verbose_name="Цена покупки")
    trade_position_end = models.FloatField(verbose_name="Цена продажи")
    signal_owner = models.CharField(verbose_name="Создатель сигнала")



    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Данные сигналов'

    def __str__(self):
        return self.cryptocode
