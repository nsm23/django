from django.db import models


class ProductCategory(models.Model):
    name = models.CharField('имя', max_length=32)
    description = models.TextField('описание', blank=True)
    is_active = models.BooleanField('active', default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория продукта'
        verbose_name_plural = 'категории продуктов'
        ordering = ['name']

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save(using=using)

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField('имя', max_length=32)
    image = models.ImageField(upload_to='products_img', blank=True)
    description = models.TextField('описание', max_length=128)
    price = models.DecimalField('цена', max_digits=12, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField('кол-во на складе', default=0)
    is_active = models.BooleanField('active', default=True)

    def __str__(self):
        return f'{self.name} / {self.category.name}'

    @classmethod
    def get_items(cls):
        return cls.objects.filter(is_active=True,
                                  category__is_active=True)

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']
