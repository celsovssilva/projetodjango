from django import forms
from .models import hellen  # Certifique-se de que 'hellen' é o nome correto do seu modelo

class TarefaForm(forms.ModelForm):
    class Meta:
        model = hellen
        fields = ('title', 'description') 