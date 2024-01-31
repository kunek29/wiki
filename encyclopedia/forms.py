from django import forms

class CreateEntryForm(forms.Form):
    title = forms.CharField(label="New Title", widget=forms.TextInput)
    content = forms.CharField(label="Content", widget=forms.Textarea)


class ExistingEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.HiddenInput)
    body = forms.CharField(label="Content", widget=forms.Textarea)