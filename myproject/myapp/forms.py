from django import forms

class SentenceForm(forms.Form):
    sentence = forms.CharField(widget=forms.Textarea)
