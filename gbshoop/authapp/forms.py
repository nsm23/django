from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import HiddenInput, forms, ModelForm

from authapp.models import GbUserProfile


class GbuserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control{field_name}'


class AgeValidatorMixin:
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and age < 18:
            raise forms.ValidationError('Подрасти, сынок!')
        return age


class GbuserCreationForm(AgeValidatorMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control{field_name}'
            field.help_text = ''


class GbuserChangeForm(AgeValidatorMixin, UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'age', 'ava')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password':
                field.widget = HiddenInput()
                continue
            field.widget.attrs['class'] = f'form-control{field_name}'
            field.help_text = ''


class GbuserProfileForm(ModelForm):
    class Meta:
        model = GbUserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'user':
                field.widget = HiddenInput()
                continue
            field.widget.attrs['class'] = f'form-control{field_name}'
