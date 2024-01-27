from django.shortcuts import render

from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from re import search


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, result):
    return render(request, "encyclopedia/entry_page.html", {
        "title": result,
        "body": util.get_entry(result)
    })

def results(request):
    result = request.GET.get('q')
    result = result.lower()

    entries = util.list_entries()

    result_list = []

    for entry in entries:
        entry = entry.lower()

        if result == entry:
            return entry_page(request, result)        
        elif result in entry:
            result_list.append(entry)
            print(result_list)
        
    return render(request, "encyclopedia/results.html", {
        "entries": result_list
    })

