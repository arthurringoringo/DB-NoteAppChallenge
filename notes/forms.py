from django import forms
from .models import Note

class CreateForm(forms.ModelForm):
    notetitle = forms.CharField(label='Note Title', max_length=55)
    notecontext = forms.CharField(widget=forms.Textarea)