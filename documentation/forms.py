from django import forms

class ErrorForm(forms.Form):
    err_name = forms.CharField(label='Название', help_text='Введите название сообщения', max_length=50, )
    err_desc = forms.CharField(label='Описание', help_text='Опишите суть ошибки', max_length=1000, widget=forms.Textarea(attrs={'rows': 4}))
    

class SearchForm(forms.Form):
    search_key = forms.CharField(label='Искать', help_text='Введите поисковое слово', max_length=30, )
