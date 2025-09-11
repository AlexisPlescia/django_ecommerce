from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile


class UserInfoForm(forms.ModelForm):
	phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Teléfono'}), required=False)
	address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección 1'}), required=False)
	address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección 2'}), required=False)
	city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ciudad'}), required=False)
	state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Provincia/Estado'}), required=False)
	zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Código Postal'}), required=False)
	country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'País'}), required=False)

	class Meta:
		model = Profile
		fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', )



class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Contraseña'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Tu contraseña no puede ser muy similar a tu información personal.</li><li>Tu contraseña debe contener al menos 8 caracteres.</li><li>Tu contraseña no puede ser una contraseña comúnmente utilizada.</li><li>Tu contraseña no puede ser completamente numérica.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirmar Contraseña'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Ingresa la misma contraseña que antes, para verificación.</small></span>'

class UpdateUserForm(UserChangeForm):
	# Hide Password stuff
	password = None
	# Get other fields
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo Electrónico'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_ .</small></span>'

		
class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo Electrónico'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_ .</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Tu contraseña no puede ser muy similar a tu información personal.</li><li>Tu contraseña debe contener al menos 8 caracteres.</li><li>Tu contraseña no puede ser una contraseña comúnmente utilizada.</li><li>Tu contraseña no puede ser completamente numérica.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar Contraseña'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Ingresa la misma contraseña que antes, para verificación.</small></span>'