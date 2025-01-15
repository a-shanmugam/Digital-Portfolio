from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Post


class BlogIndexViewTests(TestCase):

    def setUp(self):
        # Create sample posts for testing
        self.post1 = Post.objects.create(
            title="Test Post 1", body="This is the body of the first test post."
        )
        self.post2 = Post.objects.create(
            title="Test Post 2", body="This is the body of the second test post."
        )
        self.post3 = Post.objects.create(
            title="Another Test",
            body="This is a post that will not match the search query.",
        )

    def test_blog_index_view_status_code(self):
        # Reverse the URL for the blog_index view
        url = reverse("blog_index")

        # Simulate a GET request to this URL
        response = self.client.get(url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_blog_index_view_template_used(self):
        # Reverse the URL for the blog_index view
        url = reverse("blog_index")

        # Simulate a GET request
        response = self.client.get(url)

        # Check that the correct template is used
        self.assertTemplateUsed(response, "blog/index.html")

    def test_blog_index_view_context_data_no_query(self):
        # Reverse the URL for the blog_index view (no query)
        url = reverse("blog_index")

        # Simulate a GET request
        response = self.client.get(url)

        # Check that all posts are in the context
        self.assertIn(self.post1, response.context["posts"])
        self.assertIn(self.post2, response.context["posts"])
        self.assertIn(self.post3, response.context["posts"])

    def test_blog_index_view_context_data_with_query(self):
        # Reverse the URL for the blog_index view with a search query
        url = reverse("blog_index") + "?query=Test Post"

        # Simulate a GET request with a search query
        response = self.client.get(url)

        # Check that only posts with 'Test Post' in the title or body are returned
        self.assertIn(self.post1, response.context["posts"])
        self.assertIn(self.post2, response.context["posts"])
        self.assertNotIn(self.post3, response.context["posts"])

    def test_blog_index_view_empty_query(self):
        # Reverse the URL for the blog_index view with an empty query
        url = reverse("blog_index") + "?query="

        # Simulate a GET request with an empty query
        response = self.client.get(url)

        # Check that all posts are displayed (since the query is empty)
        self.assertIn(self.post1, response.context["posts"])
        self.assertIn(self.post2, response.context["posts"])
        self.assertIn(self.post3, response.context["posts"])

    def test_blog_index_view_no_matches_for_query(self):
        # Reverse the URL for the blog_index view with a search query that matches no posts
        url = reverse("blog_index") + "?query=Nonexistent Post"

        # Simulate a GET request with a search query
        response = self.client.get(url)

        # Check that no posts are returned for this query
        self.assertEqual(len(response.context["posts"]), 0)


class BlogCategoryViewTests(TestCase):

    def setUp(self):
        # Create categories for testing
        self.category1 = Category.objects.create(name="Tech")
        self.category2 = Category.objects.create(name="Lifestyle")

        # Create sample posts for testing
        self.post1 = Post.objects.create(
            title="Tech Post 1",
            body="This is a tech post.",
        )
        self.post1.categories.set([self.category1])

        self.post2 = Post.objects.create(title="Tech Post 2", body="Another tech post.")
        self.post2.categories.set([self.category1])

        self.post3 = Post.objects.create(
            title="Lifestyle Post",
            body="This is a lifestyle post.",
        )
        self.post3.categories.set([self.category2])

    def test_blog_category_view_status_code(self):
        # Reverse the URL for the blog_category view (use category name 'Tech')
        url = reverse("blog_category", kwargs={"category": "Tech"})

        # Simulate a GET request to this URL
        response = self.client.get(url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_blog_category_view_template_used(self):
        # Reverse the URL for the blog_category view (use category name 'Tech')
        url = reverse("blog_category", kwargs={"category": "Tech"})

        # Simulate a GET request
        response = self.client.get(url)

        # Check that the correct template is used
        self.assertTemplateUsed(response, "blog/category.html")

    def test_blog_category_view_context_data(self):
        # Reverse the URL for the blog_category view (use category name 'Tech')
        url = reverse("blog_category", kwargs={"category": "Tech"})

        # Simulate a GET request
        response = self.client.get(url)

        # Check that the category passed in the context is correct
        self.assertEqual(response.context["category"], "Tech")

        # Check that the posts in the context are filtered by category
        self.assertIn(self.post1, response.context["posts"])
        self.assertIn(self.post2, response.context["posts"])
        self.assertNotIn(self.post3, response.context["posts"])

    def test_blog_category_view_no_posts(self):
        # Reverse the URL for a category that has no posts (e.g., 'Health')
        url = reverse("blog_category", kwargs={"category": "Health"})

        # Simulate a GET request
        response = self.client.get(url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the context contains an empty list of posts
        self.assertEqual(len(response.context["posts"]), 0)


class BlogDetailViewTests(TestCase):
    def setUp(self):
        # Create a sample post for testing
        self.post = Post.objects.create(
            title="Test Post", body="This is a test post for the blog detail view."
        )

    def test_blog_detail_view_status_code(self):
        # Reverse the URL of the blog_detail view (using the post's pk)
        url = reverse("blog_detail", kwargs={"pk": self.post.pk})

        # Use the client to simulate a GET request
        response = self.client.get(url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_view_template_used(self):
        # Reverse the URL of the blog_detail view (using the post's pk)
        url = reverse("blog_detail", kwargs={"pk": self.post.pk})

        # Use the client to simulate a GET request
        response = self.client.get(url)

        # Check that the correct template is used for the view
        self.assertTemplateUsed(response, "blog/detail.html")

    def test_blog_detail_view_context_data(self):
        # Reverse the URL of the blog_detail view (using the post's pk)
        url = reverse("blog_detail", kwargs={"pk": self.post.pk})

        # Use the client to simulate a GET request
        response = self.client.get(url)

        # Check that the correct context is passed to the template
        self.assertEqual(response.context["post"], self.post)


class CategoryModelTests(TestCase):

    def test_category_creation(self):
        # Create a new category
        category = Category.objects.create(name="Tech")

        # Ensure it is saved correctly
        self.assertEqual(category.name, "Tech")
        self.assertEqual(Category.objects.count(), 1)

    def test_category_str(self):
        # Create a category
        category = Category.objects.create(name="Tech")

        # Ensure the string representation is correct
        self.assertEqual(str(category), "Tech")


class PostModelTests(TestCase):

    def setUp(self):
        # Set up initial data: create categories
        self.category_tech = Category.objects.create(name="Tech")
        self.category_lifestyle = Category.objects.create(name="Lifestyle")

        # Create a post associated with categories
        self.post = Post.objects.create(
            title="Test Post",
            body="This is the body of the test post.",
            created_on=timezone.now(),
            last_modified=timezone.now(),
        )
        self.post.categories.add(self.category_tech, self.category_lifestyle)

    def test_post_creation(self):
        # Check if the post was created successfully
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.body, "This is the body of the test post.")
        self.assertEqual(
            post.categories.count(), 2
        )  # Check the many-to-many relationship

        # Check that the post is correctly associated with categories
        self.assertIn(self.category_tech, post.categories.all())
        self.assertIn(self.category_lifestyle, post.categories.all())

    def test_post_str(self):
        # Ensure the string representation is correct
        self.assertEqual(str(self.post), "Test Post")

    def test_post_categories(self):
        # Ensure that the categories are correctly added and retrieved
        self.assertIn(self.category_tech, self.post.categories.all())
        self.assertIn(self.category_lifestyle, self.post.categories.all())

    def test_post_image_field(self):
        # Create a post with an image (mocking image file upload)
        post_with_image = Post.objects.create(
            title="Post with Image",
            body="This post has an image.",
            created_on=timezone.now(),
            last_modified=timezone.now(),
            image="post_images/sample_image.jpg",  # Simulate an image file path
        )

        # Ensure the post is created with an image
        self.assertEqual(post_with_image.image, "post_images/sample_image.jpg")
