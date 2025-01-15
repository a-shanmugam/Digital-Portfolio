from django.contrib import admin
from projects.models import Project


class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(
    Project, ProjectAdmin
)  # register the Project model in the admin site
