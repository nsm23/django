import hashlib
from datetime import timedelta
import random

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse

from django.utils.timezone import now

from gbshoop.settings import DOMAIN_NAME, ACTIVATION_KEY_TTL, EMAIL_HOST_USER


def calc_activation_key():
    return now() + timedelta(hours=ACTIVATION_KEY_TTL)


class Gbuser(AbstractUser):
    age = models.PositiveIntegerField('возраст', null=True)
    ava = models.ImageField(upload_to='avatars', blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    registered = models.DateTimeField(auto_now_add=True, null=True)

    def basket_price(self):
        return sum(el.product_cost for el in self.basket_set.all())

    def basket_qty(self):
        return sum(el.qty for el in self.basket_set.all())

    @property
    def is_activation_key_expired(self):
        return now() - self.registered > timedelta(hours=ACTIVATION_KEY_TTL)

    def set_activation_key(self):
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        self.activation_key = hashlib.sha1((self.email + salt).encode('utf8')).hexdigest()

    def send_confirm_email(self):
        verify_link = reverse('auth:verify',
                              kwargs={'email': self.email,
                                      'activation_key': self.activation_key})

        subject = f'Подтверждение учетной записи {self.username}'
        message = f'Для подтверждения учетной записи {self.username} на портале ' \
                  f'{DOMAIN_NAME} перейдите по ссылке: \n{DOMAIN_NAME}{verify_link}'

        return send_mail(subject, message, EMAIL_HOST_USER, [self.email],
                         fail_silently=False)


class GbUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    GENDER_CHOICES = (
        (MALE, 'man'),
        (FEMALE, 'woman')
    )

    user = models.OneToOneField(Gbuser, primary_key=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='tags', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='about me', blank=True)
    gender = models.CharField(verbose_name='gender', max_length=1, choices=GENDER_CHOICES, blank=True)

