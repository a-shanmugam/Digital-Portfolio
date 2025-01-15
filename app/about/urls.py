from django.urls import path

from . import views
from .views import ContactView, SuccessView

urlpatterns = [
    path("", views.index, name="index"),
    path("cv/", views.cv, name="cv"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("success/", SuccessView.as_view(), name="success"),
]
