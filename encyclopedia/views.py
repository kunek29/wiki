from django.shortcuts import render

from . import util
from django import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, result):
    return render(request, "encyclopedia/entry_page.html", {
        "title": result,
        "body": util.get_entry(result)
    })

