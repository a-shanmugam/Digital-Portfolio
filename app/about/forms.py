from django import forms


class ContactForm(
    forms.Form
):  # the definition of the contact form containing a name, e-mail address and a message field
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Name"}))
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Your e-mail"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Your message"})
    )
