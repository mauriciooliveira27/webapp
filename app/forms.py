from django import forms

from .models import RegistroPlaca


class PlacaForm(forms.ModelForm):

    class Meta:
        model = RegistroPlaca
        fields = '__all__'  