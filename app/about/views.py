from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, reverse
from django.views.generic import FormView, TemplateView

from .forms import ContactForm


def index(request):  # index view of the "about me"-page, which is just the template
    return render(request, "about/index.html")


def cv(request):  # cv view of the "about me"-page, which is just the template
    return render(request, "about/cv.html")


class SuccessView(
    TemplateView
):  # success view of the "about me"-page, which is just the template
    template_name = "about/success.html"


class ContactView(FormView):  # contact form
    form_class = ContactForm
    template_name = "about/contact.html"

    def get_success_url(
        self,
    ):  # register the success view as a redirect after successful submission of the form
        return reverse("success")

    def form_valid(self, form):
        name = form.cleaned_data.get("name")
        email = form.cleaned_data.get("email")
        message = form.cleaned_data.get("message")

        full_message = f"""
            Message below was sent by {name} ({email})
            ________________________


            {message}
            """
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        return super(ContactView, self).form_valid(form)
