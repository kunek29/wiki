from django.shortcuts import render

from . import util, forms
import random
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    
    # Check if entry exists within list of entries.
    entries = util.list_entries()
    if title not in entries:
        
        # If it doesn't, return error message.
        return error_page(request, error_message="Entry doesn't exist.")

    # Otherwise:
    else:

        # Convert markdown content to html  
        markdowner = Markdown()
        body = util.get_entry(title)
        body_converted = markdowner.convert(body)
    
        # Render entry page    
        return render(request, "encyclopedia/entry_page.html", {
            "title": title,
            "body_converted": body_converted
        })


def edit_page(request, title):

    # If clicked Save button, save the entry and go to entry page.
    if request.method == "POST":
        form = forms.ExistingEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            util.save_entry(title, body)
         
            return entry_page(request, title)
        
        # If empty field, render edit page again.                
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "form": form,
                "title": title
        })

    # Make dictionary to fill form with initial values.  
    initial_dict = {
        "title": title,
        "body": util.get_entry(title)
    }

    # Render edit page with a prepopulated form.
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": forms.ExistingEntryForm(None, initial = initial_dict)
    })


def results(request):
    # Get a query
    query = request.GET.get('q')
    
    # Get a list of entries
    entries = util.list_entries()

    # Initiate a list
    result_list = []

    # Iterate through entries to check if a query matches any entry
    for entry in entries:
        
        # If a query matches entry, go to entry's page (case insensitive)
        if query.lower() == entry.lower():
            return entry_page(request, query) 
        
        # If a query is a substring of an entry, add an entry to a list of resutls (case insensitive).     
        elif query.lower() in entry.lower():
            result_list.append(entry)
    
    # Show a message if the list is empty
    if len(result_list) == 0:
        return error_page(request, error_message="No results. Try Again.")
    
    # Otherwise, render a list of results
    else:
        return render(request, "encyclopedia/results.html", {
            "entries": result_list
        })


def create_page(request):

    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = forms.CreateEntryForm(request.POST)

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
                return error_page(request, error_message="Can't create. The Entry alredy exists.")
        
        # Return to existing form if imput invalid
        else:
            return render(request, "encyclopedia/create_page", {
                "form": form
            })
    
    # Render form to create an entry
    return render(request, "encyclopedia/create_page.html", {
        "form": forms.CreateEntryForm()
    })


def error_page(request, error_message):
    return render(request, "encyclopedia/error_page.html", {
        "error": error_message
    })


def random_entry(request):

    # Pick and render a random entry from a list of entries.
    random_entry = random.choice(util.list_entries())
    return entry_page(request, random_entry)
