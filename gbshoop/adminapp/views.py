from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from adminapp.forms import AdminUserUpdateForm, ProductCategoryCreateForm, AdminProductUpdateForm
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda user: user.is_superuser)
def index(request):
    all_users = get_user_model().objects.all()
    cont = {
        'page_title': 'admin_users',
        'all_users': all_users,
    }
    return render(request, 'adminapp/index.html', cont)


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    pt_key = 'page_title'
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.pt_key] = self.page_title
        return context


class UserAdminUpdateForm(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = get_user_model()
    form_class = AdminUserUpdateForm
    success_url = reverse_lazy('new_admin:index')
    pk_url_kwarg = 'user_pk'
    page_title = 'User_update'


class UserAdminDeleteForm(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = get_user_model()
    form_class = AdminUserUpdateForm
    success_url = reverse_lazy('new_admin:index')
    pk_url_kwarg = 'user_pk'
    page_title = 'User_delete'


class ProductCategoryList(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ProductCategory
    page_title = 'Product_category'


class ProductCategoryCreate(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    form_class = ProductCategoryCreateForm
    success_url = reverse_lazy('new_admin:categories')
    page_title = 'Add_new_category'


class ProductCategoryUpdate(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    form_class = ProductCategoryCreateForm
    success_url = reverse_lazy('new_admin:categories')
    page_title = 'Update_category'


class ProductCategoryDel(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('new_admin:categories')
    page_title = 'Del_category'


@user_passes_test(lambda user: user.is_superuser)
def category_products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    object_list = category.product_set.all()
    cont = {
        'page_title': f'category {category.name}/products',
        'category': category,
        'object_list': object_list
    }
    return render(request, 'mainapp/category_products_list.html', cont)


@user_passes_test(lambda user: user.is_superuser)
def product_create(request, category_pk):
    category = get_object_or_404(ProductCategory, pk=category_pk)
    if request.method == "POST":
        form = AdminProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('new_admin:category_products', kwargs={'pk': category_pk}))
    else:
        form = AdminProductUpdateForm(
            initial={
                'category': category,
            }
        )
    cont = {
        'page_title': 'product_create',
        'form': form,
        'category': category,
    }
    return render(request, 'mainapp/product_update.html', cont)


class ProductDetail(SuperUserOnlyMixin, PageTitleMixin, DetailView):
    model = Product
    page_title = 'admin/products'

