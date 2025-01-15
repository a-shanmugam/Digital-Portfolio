from django import forms


class SearchForm(forms.Form):  # define a form with a character field for searching
    query = forms.CharField(label="Search", max_length=100, required=False)
