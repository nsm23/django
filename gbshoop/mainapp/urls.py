from django.urls import path
import mainapp.views as mainapp

app_name = 'general'

urlpatterns = [
    path('', mainapp.index, name='home'),
    path('products/', mainapp.products, name='products'),
    path('contact/', mainapp.contact, name='contact'),
    path('category/<int:pk>/', mainapp.category, name='category'),
    path('product_page/<int:pk>/', mainapp.product_page, name='product_page'),
    path('product/<int:pk>/price/', mainapp.get_product_price),
]

