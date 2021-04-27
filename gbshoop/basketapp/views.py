from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from gbshoop.settings import LOGIN_URL


@login_required
def index(request):
    basket = request.user.basket_set.all()

    cont = {
        'page': 'basket',
        'basket': basket,
    }
    return render(request, 'basketapp/index.html', cont)


@login_required
def append(request, product_pk):
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            reverse('general:product_page',
                    kwargs={'pk': product_pk}))

    basket_item, _ = Basket.objects.get_or_create(
        user=request.user,
        product_id=product_pk
    )
    basket_item.qty += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, basket_item_pk):
    item = get_object_or_404(Basket, pk=basket_item_pk)
    item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update(request, basket_item_pk, qty):
    if request.is_ajax():
        item = Basket.objects.filter(pk=basket_item_pk).first()
        if not item:
            return JsonResponse({'status': False})
        if qty == 0:
            item.delete()
        else:
            item.qty = qty
            item.save()
        basket_summary_html = render_to_string(
            'basketapp/includes/basket_summary.html', request=request)
        return JsonResponse({'status': True,
                             'basket summary': basket_summary_html,
                             'qty': qty})
