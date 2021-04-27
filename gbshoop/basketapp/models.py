from django.contrib.auth import get_user_model
from django.db import models

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField('кол-во', default=0)
    add_date = models.DateTimeField('time', auto_now_add=True)
    update_date = models.DateTimeField('time', auto_now=True)

    @property
    def product_cost(self):
        return self.product.price * self.qty


