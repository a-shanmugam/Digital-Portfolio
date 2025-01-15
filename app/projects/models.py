from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="project_images/", null=True, blank=True)

    def __str__(self):
        return self.title
