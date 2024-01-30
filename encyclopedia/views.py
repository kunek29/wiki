from django.shortcuts import render

from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from markdown2 import Markdown


class CreateEntryForm(forms.Form):
    title = forms.CharField(label="New Title", widget=forms.TextInput)
    content = forms.CharField(label="Content", widget=forms.Textarea)


class ExistingEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.HiddenInput)
    body = forms.CharField(label="Content", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    
    # If clicked Edit, render edit_page.
    if request.method == "POST":
        body = util.get_entry(title)

        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "form": ExistingEntryForm(request.POST)
        })
    # Render entry page  
    markdowner = Markdown()
    body = util.get_entry(title)
    body_converted = markdowner.convert(body)
         
    return render(request, "encyclopedia/entry_page.html", {
        "title": title,
        "body_converted": body_converted,
        "body": body
    })


def edit_page(request):

    # If clicked Save button, save the entry and go to entry page.
    if request.method == "POST":
        form = ExistingEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            util.save_entry(title, body)

            markdowner = Markdown()
            body = util.get_entry(title)
            body_converted = markdowner.convert(body)
         
            return render(request, "encyclopedia/entry_page.html", {
                "title": title,
                "body_converted": body_converted,
                "body": body
            })
        
        # If empty field, render edit page again.                
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "form": form,
                "title": title
        })

    # If not entered from entry page, show error    
    error_message = "Nothing to edit"
    return error_page(request, error_message)


def results(request):
    # Get a query
    query = request.GET.get('q')
    
    # Get a list of entries
    entries = util.list_entries()

    # Initiate a list
    result_list = []

    # Iterate through entries to check if a query matches any entry
    for entry in entries:
        
        # If a query matches entry, go to entry's page
        if query.lower() == entry.lower():
            return entry_page(request, query) 
        # If a query is a substring of an entry, add an entry to a list of resutls       
        elif query.lower() in entry.lower():
            result_list.append(entry)
    
    # Show a message if the list is empty
    if len(result_list) == 0:
        error_message = "No results. Try Again."
        return error_page(request, error_message)
    # Otherwise show a list of results
    else:
        return render(request, "encyclopedia/results.html", {
            "entries": result_list
        })


def create_page(request):

    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = CreateEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            
            # Isolate the title
            title = form.cleaned_data["title"]
            entries = util.list_entries()
            
            # Check if a title already exists
            if title not in entries:
                
                # If not, isolate content, save the entry and go to entry's page
                content = form.cleaned_data['content']
                util.save_entry(title, content)
                return entry_page(request, title)
            
            # Otherwise, show an error message
            else:
                error_message = "The Entry alredy exists"
                return error_page(request, error_message)
        
        # Return to form if invalid
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


def random_entry(request):

    entries = util.list_entries()
    random_entry = random.choice(entries)
    return entry_page(request, random_entry)

    

                  
