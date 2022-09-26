from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
from wiki import encyclopedia


def index(request):
    #TODO: right now, searching can only be done from the index page, later this needs to be updated so it can be done from othe pages as well.
    if request.method == "POST":
        title_name = request.POST.get("q")
        if util.get_entry(title_name):
            return render(request, "encyclopedia/entry.html", {
                "entries" : util.get_entry(title_name)
            })
        else:
            sub_list = []
            main_list = util.list_entries()
            print(main_list)

            for item in main_list:
                if title_name.lower() in item.lower():
                    sub_list.append(item)

            if not sub_list:
                return render(request, "encyclopedia/error.html", {
                    "message" : "Requested page was not found."
                })
            return render(request, "encyclopedia/index.html", {
                "entries" : sub_list
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title_name):
    if not util.get_entry(title_name):
        return render(request, "encyclopedia/error.html", {
            "message" : "Requested page was not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title_name" : title_name,
        "entries" : util.get_entry(title_name)
    })

def new_page(request):
    if request.method == "POST":
        title_name = request.POST.get("title")
        md_content = request.POST.get("md_content")
        if not title_name:
            return render(request, "encyclopedia/error.html", {
                "message" : "Must provide a title."
            })
        
        print(len(md_content))
        if not md_content:
            return render(request, "encyclopedia/error.html", {
                "message" : "Must provide markdown content for the page."
            })
        
        existing_titles = util.list_entries()
        if title_name in existing_titles:
            return render(request, "encyclopedia/error.html",{
                "message" : "Another page with the same title already exists. Please choose another one."
            })

        util.save_entry(title_name, md_content)
        #TODO: Redirecting user to home for now, but need to redirect user to the page they just created.
        return redirect('/')
        
    return render(request, "encyclopedia/new_page.html")

def edit_page():
    return render(request, "encyclopedia/edit_page.html")
