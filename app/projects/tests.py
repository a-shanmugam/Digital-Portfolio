from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Project


class ProjectIndexViewTests(TestCase):

    def setUp(self):
        # Create sample projects for testing
        self.project1 = Project.objects.create(
            title="Test Project 1", body="This is the body of the first test project."
        )
        self.project2 = Project.objects.create(
            title="Test Project", body="This is the body of the second test project."
        )
        self.project3 = Project.objects.create(
            title="Another Test",
            body="This is a project that will not match the search query.",
        )

    def test_project_index_view_status_code(self):
        # Reverse the URL for the project_index view
        url = reverse("project_index")

        # Simulate a GET request to this URL
        response = self.client.get(url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_project_index_view_template_used(self):
        # Reverse the URL for the project_index view
        url = reverse("project_index")

        # Simulate a GET request
        response = self.client.get(url)

        # Check that the correct template is used
        self.assertTemplateUsed(response, "projects/index.html")

    def test_project_index_view_context_data_no_query(self):
        # Reverse the URL for the project_index view (no query)
        url = reverse("project_index")

        # Simulate a GET request
        response = self.client.get(url)

        # Check that all projects are in the context
        self.assertIn(self.project1, response.context["projects"])
        self.assertIn(self.project2, response.context["projects"])
        self.assertIn(self.project3, response.context["projects"])

    def test_project_index_view_context_data_with_query(self):
        # Reverse the URL for the project_index view with a search query
        url = reverse("project_index") + "?query=Test Project"

        # Simulate a GET request with a search query
        response = self.client.get(url)

        # Check that only projects with 'Test Project' in the title or body are returned
        self.assertIn(self.project1, response.context["projects"])
        self.assertIn(self.project2, response.context["projects"])
        self.assertNotIn(self.project3, response.context["projects"])

    def test_project_index_view_empty_query(self):
        # Reverse the URL for the project_index view with an empty query
        url = reverse("project_index") + "?query="

        # Simulate a GET request with an empty query
        response = self.client.get(url)

        # Check that all projects are displayed (since the query is empty)
        self.assertIn(self.project1, response.context["projects"])
        self.assertIn(self.project2, response.context["projects"])
        self.assertIn(self.project3, response.context["projects"])

    def test_project_index_view_no_matches_for_query(self):
        # Reverse the URL for the project_index view with a search query that matches no projects
        url = reverse("project_index") + "?query=Nonexistent Project"

        # Simulate a GET request with a search query
        response = self.client.get(url)

        # Check that no projects are returned for this query
        self.assertEqual(len(response.context["projects"]), 0)


class ProjectDetailViewTests(TestCase):
    def setUp(self):
        # Create a sample project for testing
        self.project = Project.objects.create(
            title="Test Project",
            body="This is a test project for the project detail view.",
        )

    def test_project_detail_view_status_code(self):
        # Reverse the URL of the project_detail view (using the project's pk)
        url = reverse("project_detail", kwargs={"pk": self.project.pk})

        # Use the client to simulate a GET request
        response = self.client.get(url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_project_detail_view_template_used(self):
        # Reverse the URL of the project_detail view (using the project's pk)
        url = reverse("project_detail", kwargs={"pk": self.project.pk})

        # Use the client to simulate a GET request
        response = self.client.get(url)

        # Check that the correct template is used for the view
        self.assertTemplateUsed(response, "projects/detail.html")

    def test_project_detail_view_context_data(self):
        # Reverse the URL of the project_detail view (using the project's pk)
        url = reverse("project_detail", kwargs={"pk": self.project.pk})

        # Use the client to simulate a GET request
        response = self.client.get(url)

        # Check that the correct context is passed to the template
        self.assertEqual(response.context["project"], self.project)


class ProjectModelTests(TestCase):

    def setUp(self):
        # Create a project associated with categories
        self.project = Project.objects.create(
            title="Test project",
            body="This is the body of the test project.",
            created_on=timezone.now(),
            last_modified=timezone.now(),
        )

    def test_project_creation(self):
        # Check if the project was created successfully
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.title, "Test project")
        self.assertEqual(project.body, "This is the body of the test project.")

    def test_project_str(self):
        # Ensure the string representation is correct
        self.assertEqual(str(self.project), "Test project")

    def test_project_image_field(self):
        # Create a project with an image (mocking image file upload)
        project_with_image = Project.objects.create(
            title="Project with Image",
            body="This project has an image.",
            created_on=timezone.now(),
            last_modified=timezone.now(),
            image="project_images/sample_image.jpg",  # Simulate an image file path
        )

        # Ensure the project is created with an image
        self.assertEqual(project_with_image.image, "project_images/sample_image.jpg")
