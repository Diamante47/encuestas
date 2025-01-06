from django import forms
from .models import Encuesta, Pregunta, Respuesta

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['titulo', 'descripcion']


class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto']


class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['texto']
