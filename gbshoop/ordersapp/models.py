from django.contrib.auth import get_user_model
from django.db import models

from mainapp.models import Product


class Order(models.Model):
    STATUS_FORMING = 'F'
    STATUS_PAID = 'P'
    STATUS_SENDED = 'S'
    STATUS_DELETED = 'D'

    STATUS_CHOICES = (
        (STATUS_FORMING, 'forming'),
        (STATUS_PAID, 'paid'),
        (STATUS_SENDED, 'sent'),
        (STATUS_DELETED, 'deleted'),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='orders')
    add_date = models.DateTimeField('time', auto_now_add=True)
    update_date = models.DateTimeField('time', auto_now=True)
    status = models.CharField('status', max_length=1,
                              choices=STATUS_CHOICES,
                              default=STATUS_FORMING)
    is_active = models.BooleanField(verbose_name='active', default=True)

    @property
    def is_forming(self):
        return self.status == self.STATUS_FORMING

    @property
    def total_quantity(self):
        return sum(map(lambda x: x.qty, self.items.all()))

    @property
    def total_cost(self):
        return sum(map(lambda x: x.product_cost, self.items.all()))

    def delete(self, using=None, keep_parents=False):
        for item in self.items.all():
            item.product.quantity += item.qty
            item.product.save()
        self.is_active = False
        self.save()

    class Meta:
        ordering = ('-add_date',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderItemManager(models.QuerySet):
    def delete(self):
        for item in self:
            item.delete()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField('кол-во', default=0)
    add_date = models.DateTimeField('time', auto_now_add=True)
    update_date = models.DateTimeField('time', auto_now=True)

    @property
    def product_cost(self):
        return self.product.price * self.qty


    @classmethod
    def get_item(cls, pk):
        return cls.objects.filter(pk=pk).first()
