# from django.http import HttpResponse
from blog.models import Post
from django.shortcuts import render

from .forms import SearchForm


def blog_index(request):
    """The index view of the 'blog'-page

    Parameters
    ----------
    :param request:
        the incoming HTML request
    :return:
        the rendered content
    """
    posts = Post.objects.all().order_by("-created_on")  # get all Post objects
    form = SearchForm(request.GET)  # create SearchForm object
    if form.is_valid():  # update the context if a valid form has been submitted
        query = form.cleaned_data["query"]
        if query:
            # Filter posts based on the query in title and body
            posts = posts.filter(title__icontains=query) | posts.filter(
                body__icontains=query
            )

    context = {
        "form": form,
        "posts": posts,
    }
    return render(request, "blog/index.html", context)


def blog_category(request, category):
    """The view displaying a list of all posts within one selected category

    Parameters
    ----------
    :param request:
        the incoming HTML request
    :param category:
        the selected category to be displayed
    :return:
        the rendered content
    """
    posts = Post.objects.filter(categories__name__contains=category).order_by(
        "-created_on"
    )  # select all posts within the selected category

    context = {  # update the context
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


def blog_detail(request, pk):
    """The detail view, displaying the details of a specific post

    Parameters
    ----------
    :param request:
        the incoming HTML request
    :param pk:
        primary key of the selected post
    :return:
        the rendered content
    """
    post = Post.objects.get(pk=pk)
    context = {
        "post": post,
    }
    return render(request, "blog/detail.html", context)
