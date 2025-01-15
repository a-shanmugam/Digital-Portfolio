from django.shortcuts import render
from projects.models import Project

from .forms import SearchForm


def project_index(request):
    """The index view of the 'projects'-page, displaying a list of projects

    Parameters
    ----------
    :param request:
        the incoming HTML request
    :return:
        the rendered content
    """
    projects = Project.objects.all().order_by(
        "-created_on"
    )  # retrieve all project objects
    form = SearchForm(request.GET)  # create a SearchForm object

    if form.is_valid():  # update the context if a valid form has been submitted
        query = form.cleaned_data["query"]
        if query:
            # Filter projects based on the query in title and body
            projects = projects.filter(title__icontains=query) | projects.filter(
                body__icontains=query
            )

    context = {
        "form": form,
        "projects": projects,
    }
    return render(request, "projects/index.html", context)


def project_detail(request, pk):
    """The detail view, displaying the details of a specific project

    Parameters
    ----------
    :param request:
        the incoming HTML request
    :param pk:
        the primary key of a project
    :return:
        the rendered content
    """
    project = Project.objects.get(pk=pk)  # get specific project
    context = {  # update the context
        "project": project,
    }
    return render(request, "projects/detail.html", context)
