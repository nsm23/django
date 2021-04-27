from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.forms import HiddenInput, ModelForm

from authapp.forms import AgeValidatorMixin
from mainapp.models import ProductCategory, Product


class AdminUserUpdateForm(AgeValidatorMixin, UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'password', 'email',
                  'age', 'ava', 'is_staff', 'is_superuser', 'is_active')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = f'form-control {field_name}'
                field.help_text = ''
                if field_name == 'password':
                    field.widget = HiddenInput()


class ProductCategoryCreateForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'category':
                field.widget = HiddenInput()


class AdminProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'category':
                field.widget = HiddenInput()
