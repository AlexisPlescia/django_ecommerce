from django import forms
from .models import ShippingAddress, ShippingMethod, ShippingMethod


class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo'
        }),
        required=True
    )
    shipping_email = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        }),
        required=True
    )
    shipping_address1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dirección'
        }),
        required=True
    )
    shipping_city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ciudad'
        }),
        required=True
    )
    shipping_state = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Provincia / Estado'
        }),
        required=False
    )
    shipping_zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código postal'
        }),
        required=False
    )

    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_full_name',
            'shipping_email',
            'shipping_address1',
            'shipping_city',
            'shipping_state',
            'shipping_zipcode',
        ]
        exclude = ['user',]


class PaymentForm(forms.Form):
    card_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre en la tarjeta'
        }),
        required=True
    )
    card_number = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de tarjeta'
        }),
        required=True
    )
    card_exp_date = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Fecha de vencimiento'
        }),
        required=True
    )
    card_cvv_number = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código CVV'
        }),
        required=True
    )
    card_address1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dirección de facturación 1'
        }),
        required=True
    )
    card_address2 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dirección de facturación 2'
        }),
        required=False
    )
    card_city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ciudad de facturación'
        }),
        required=True
    )
    card_state = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Provincia / Estado de facturación'
        }),
        required=True
    )
    card_zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Código postal de facturación'
        }),
        required=True
    )
    card_country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'País de facturación'
        }),
        required=True
    )


# Formulario para seleccionar método de envío
class ShippingMethodForm(forms.Form):
    shipping_method = forms.ModelChoiceField(
        queryset=ShippingMethod.objects.filter(is_active=True),
        label="Método de Envío",
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        required=True,
        empty_label=None
    )

    def __init__(self, *args, **kwargs):
        cart_total = kwargs.pop('cart_total', 0)
        super().__init__(*args, **kwargs)

        # Personalizar las opciones para mostrar costos
        choices = []
        for method in ShippingMethod.objects.filter(is_active=True):
            cost = method.calculate_cost(cart_total)
            if cost == 0:
                cost_text = "GRATIS"
            else:
                cost_text = f"${cost}"

            label = f"{method.get_name_display()} - {cost_text} ({method.estimated_days})"
            choices.append((method.id, label))

        self.fields['shipping_method'].choices = choices

