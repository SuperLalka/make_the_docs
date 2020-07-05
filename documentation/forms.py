from django import forms
from django.utils.translation import gettext_lazy as _

class ErrorForm(forms.Form):
    err_name = forms.CharField(label=_('Name'), help_text=_('Enter a message name'), max_length=50, )
    err_desc = forms.CharField(label=_('Description'), help_text=_('Describe the error'), max_length=1000, widget=forms.Textarea(attrs={'rows': 4}))
    

class SearchForm(forms.Form):
    search_key = forms.CharField(label=_('Search by'), help_text=_('Enter a search term'), max_length=30, )
