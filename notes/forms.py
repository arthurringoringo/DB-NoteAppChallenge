from django import forms
from .models import Note
from django.forms import ModelForm

class CreateForm(forms.ModelForm):
    note_title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    context = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'4'}))
    class Meta:
        model = Note
        fields = 'note_title','context'