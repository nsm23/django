from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),

    path('user/delete/<int:user_pk>', adminapp.UserAdminDeleteForm.as_view(),
         name='user_delete'),
    path('user/update_form/<int:user_pk>/', adminapp.UserAdminUpdateForm.as_view(),
         name='user_update'),

    path('categories/', adminapp.ProductCategoryList.as_view(),
         name='categories'),
    path('category/create/', adminapp.ProductCategoryCreate.as_view(),
         name='category_create'),
    path('category/update/<int:pk>/', adminapp.ProductCategoryUpdate.as_view(),
         name='category_update'),
    path('category/del/<int:pk>/', adminapp.ProductCategoryDel.as_view(),
         name='category_delete'),
    path('category/<int:pk>/products/', adminapp.category_products,
         name='category_products'),
        path('category/<int:category_pk>/product/create/', adminapp.product_create,
         name='product_create'),

    path('product/<int:pk>/', adminapp.ProductDetail.as_view(),
         name='product_view'),
]

