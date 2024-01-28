from django.shortcuts import render

from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from re import search


class CreateEntryForm(forms.Form):
    title = forms.CharField(label="New Title", widget=forms.TextInput)
    content = forms.CharField(label= "Content", widget=forms.Textarea)


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
        
    if len(result_list) == 0:
        error_message = "No results. Try Again."
        return error_page(request, error_message)
    else:
        return render(request, "encyclopedia/results.html", {
            "entries": result_list
        })


def create_page(request):

    if request.method == "POST":

        form = CreateEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            entries = util.list_entries()

            if title not in entries:
                
                content = form.cleaned_data['content']

                util.save_entry(title, content)

                return entry_page(request, title)
            else:
                error_message = "The Entry alredy exists"
                return error_page(request, error_message)
        else:
            return render(request, "encyclopedia/create_page", {
                "form": form
            })
    
    
    return render(request, "encyclopedia/create_page.html", {
        "form": CreateEntryForm()
    })


def error_page(request, error_message):
    return render(request, "encyclopedia/error_page.html", {
        "error": error_message
    })
