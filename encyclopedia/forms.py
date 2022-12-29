from django import forms
from django.forms import ModelForm
from .models import Entry

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ('entry_title','entry_content')
        labels = {
            'entry_title': '',
            'entry_content': '',
        }
        widgets = {
            'entry_title': forms.TextInput(attrs={'placeholder':'Title'}),
            'entry_content': forms.Textarea(attrs={'placeholder':'Content'}),
        }