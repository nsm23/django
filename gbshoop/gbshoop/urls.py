from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from gbshoop import settings

urlpatterns = [
    path('', include('mainapp.urls', namespace='general')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('new/admin', include('adminapp.urls', namespace='new_admin')),
    path('orders/', include('ordersapp.urls', namespace='orders')),

    path('admin/', admin.site.urls),

    path('social/', include('social_django.urls', namespace='social')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

