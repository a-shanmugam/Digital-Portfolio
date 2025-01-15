from django.test import TestCase
from django.urls import reverse

from .forms import ContactForm


class IndexViewTests(TestCase):

    def test_index_view_status_code(self):
        """Test if the index view returns a 200 status code"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        """Test if the index view uses the correct template"""
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "about/index.html")


class CvViewTests(TestCase):

    def test_cv_view_status_code(self):
        """Test if the cv view returns a 200 status code"""
        response = self.client.get(reverse("cv"))
        self.assertEqual(response.status_code, 200)

    def test_cv_view_template(self):
        """Test if the cv view uses the correct template"""
        response = self.client.get(reverse("cv"))
        self.assertTemplateUsed(response, "about/cv.html")


class ContactViewTests(TestCase):

    def test_contact_view_status_code(self):
        """Test if the contact view returns a 200 status code"""
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form method="post">')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="message"')

    def test_contact_view_template(self):
        """Test if the contact view uses the correct template"""
        response = self.client.get(reverse("contact"))
        self.assertTemplateUsed(response, "about/contact.html")

    def test_form_valid_submission(self):
        """Test that the form processes valid input correctly"""
        valid_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "message": "Hello, this is a test message.",
        }
        form = ContactForm(data=valid_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse("contact"), data=valid_data)
        self.assertRedirects(response, "/success/")

    def test_form_invalid_submission(self):
        """Test that the form handles invalid input correctly"""
        invalid_data = {
            "name": "",  # Empty name field should be invalid
            "email": "not-an-email",  # Invalid email address
            "message": "",  # Empty message field should be invalid
        }
        form = ContactForm(data=invalid_data)
        self.assertFalse(form.is_valid())


class SuccessViewTests(TestCase):

    def test_success_view_status_code(self):
        """Test if the success view returns a 200 status code"""
        response = self.client.get(reverse("success"))
        self.assertEqual(response.status_code, 200)

    def test_success_view_template(self):
        """Test if the success view uses the correct template"""
        response = self.client.get(reverse("success"))
        self.assertTemplateUsed(response, "about/success.html")
