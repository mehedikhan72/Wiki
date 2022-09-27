from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

from . import util


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
        
        if not md_content:
            return render(request, "encyclopedia/error.html", {
                "message" : "Must provide markdown content for the page."
            })
        

        existing_titles = util.list_entries()
        for item in existing_titles:
            if title_name.lower() == item.lower():
                return render(request, "encyclopedia/error.html",{
                    "message" : "Another page with the same title already exists. Please choose another one."
                })

        util.save_entry(title_name, md_content)
        #TODO: Redirecting user to home for now, but need to redirect user to the page they just created.
        return redirect('/')
        
    return render(request, "encyclopedia/new_page.html")

def edit_page(request):
    if request.method == "POST":
        md_content = request.POST.get("md_content")
        title_name = request.POST.get("title")

        if not md_content:
            return render(request, "encyclopedia/error.html",{
                "message" : "Must provide md_content."
            })
        util.save_entry(title_name, md_content)
        return redirect('/')
        
    pre_url = request.META.get('HTTP_REFERER')
    title_name = ""
    for i in range(len(pre_url)):
        if i > 26 and i < len(pre_url) - 1:
            title_name += pre_url[i]

    md_content = util.get_entry(title_name)
    return render(request, "encyclopedia/edit_page.html",{
        "title_name" : title_name,
        "md_content" : md_content
    })


# It is very logical to not let the user edit the page from random page cause if you wanted to edit 
# a specific page, you wouldn't go to the random page.(but deep down, we all know I just couldn't figure a way out to do so.)

def random_page(request):
    existing_titles = util.list_entries()
    random_title = random.choice(existing_titles)
    print(random_title)
    return render(request, "encyclopedia/entry2.html", {
        "title_name" : random_title,
        "entries" : util.get_entry(random_title)
    })