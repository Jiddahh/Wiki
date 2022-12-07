from audioop import reverse
from cProfile import label
# from re import search
import re
from turtle import title
from django.shortcuts import render

from . import util

from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
import urllib.parse
import random
import markdown2
# import markdown

# markdown.markdownFromFile(
#     input='input.md',
#     output='output.html',
#     encoding='utf8',
# )
url_title = []
entries = util.list_entries()

class QueryForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Search Encyclopedia",
        "class": "search"
    }), label='')

class TitleForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Title of your new encyclopedia entry",
        "class": "titleForm"
    }), label='')

class NewPageForm(forms.Form):
    new_page = forms.CharField(widget=forms.Textarea(attrs={
        "rows": 8,
        "cols": 30,
        "placeholder": "Enter markdown content for new encyclopedia entry",
        "class": "newPageForm"
    }),label='')

class EditPageForm(forms.Form):
    edit_page = forms.CharField(widget=forms.Textarea(attrs={
        "rows": 8,
        "cols": 30,
        "class": "editForm"
    }),label='')

def index(request):
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search"]
            query = str(query)
            matches = []
            for entry in entries:
                if entry.lower() == query.lower():
                    return HttpResponseRedirect(reverse('get_entries', args=(), kwargs={'title': entry}))
                else:
                    result = (re.search(query, entry, re.IGNORECASE))
                    if result != None:
                        matches.append(entry)

            return render(request, "encyclopedia/searchResults.html", {
                "entries": matches
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": QueryForm()
    })

def get_entries(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html")

    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(title))
        })

def create_new_page(request):
    if request.method == "POST":

        form = TitleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            title = str(title)

        form = NewPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["new_page"]

        for entry in entries:
            if entry.lower() == title.lower():
                messages.error(request, 'Entry with this title alredy exists')
                return HttpResponseRedirect(reverse('create_new_page'))
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('get_entries', args=(), kwargs={'title': title}))
            
    return render(request, "encyclopedia/CreateNewPage.html", {
        "title_form": TitleForm(),
        "newpage_form": NewPageForm()
    })

def edit_page(request):
    previous_url = request.META.get('HTTP_REFERER')
    previous_url = urllib.parse.unquote(previous_url)
    url_title.append(previous_url)
    url_path = (urllib.parse.urlparse(url_title[0])).path.rsplit("/", 1)[-1]
    title = re.sub(r"\.md$", "", url_path)
    # title = request.POST.get('')
    content = util.get_entry(title)

    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["edit_page"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('get_entries', args=(), kwargs={'title': title}))

    return render(request, "encyclopedia/edit.html", {
        "edit_page_form": EditPageForm(initial={"edit_page": content})
    })

def random_page(request):
    title = random.choice(entries)
    return render(request, "encyclopedia/entry.html", {
            "entry": util.get_entry(title)
        })


