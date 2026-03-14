"""
============================================================
forms.py - Formularios de Django
============================================================
Los formularios de Django:
  1. Generan el HTML del formulario automáticamente
  2. Validan los datos enviados por el usuario
  3. Convierten los datos al tipo Python correcto
  4. Protegen contra ataques XSS y SQL Injection

ModelForm: genera un formulario directamente desde un modelo.
Es la forma más eficiente porque no repetimos la definición
de campos (principio DRY: Don't Repeat Yourself).
============================================================
"""

from django import forms
from .models import Cliente, Cuenta, Transaccion


# ============================================================
# Formulario de Cliente
# ============================================================
class ClienteForm(forms.ModelForm):
    """
    Formulario para crear y editar clientes.
    ModelForm lee la definición del modelo Cliente y genera
    los campos del formulario automáticamente.
    """

    class Meta:
        # model: ¿de qué modelo se generan los campos?
        model = Cliente

        # fields: ¿qué campos incluir? ('__all__' incluiría todos)
        # Excluimos fecha_registro porque se asigna automáticamente
        fields = ['nombre', 'email', 'telefono', 'activo']

        # widgets: personaliza el HTML que genera cada campo
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',       # Clase Bootstrap
                'placeholder': 'Ej: Ana García'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ana@gmail.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: +56 9 1234 5678'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        # labels: personaliza las etiquetas de los campos
        labels = {
            'nombre': 'Nombre completo',
            'email': 'Correo electrónico',
            'telefono': 'Número de teléfono (opcional)',
            'activo': 'Cliente activo',
        }

    def clean_email(self):
        """
        Validación personalizada del campo email.
        Los métodos clean_<campo> se ejecutan durante la validación.
        Aquí convertimos el email a minúsculas para consistencia.
        """
        email = self.cleaned_data.get('email')
        if email:
            return email.lower()
        return email


# ============================================================
# Formulario de Cuenta
# ============================================================
class CuentaForm(forms.ModelForm):
    """
    Formulario para crear y editar cuentas digitales.
    """

    class Meta:
        model = Cuenta
        fields = ['cliente', 'numero_cuenta', 'tipo', 'saldo', 'activa']

        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'numero_cuenta': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: CTA-001'
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'saldo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ============================================================
# Formulario de Transacción
# ============================================================
class TransaccionForm(forms.ModelForm):
    """
    Formulario para registrar transacciones.
    Las transacciones no deben editarse, solo crearse.
    """

    class Meta:
        model = Transaccion
        fields = ['cuenta', 'tipo', 'monto', 'descripcion']

        widgets = {
            'cuenta': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01',
                'placeholder': 'Ej: 50000'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción opcional de la transacción'
            }),
        }
