from random import randint
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django import forms

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Title", "class": "mb-4"}
        ),
    )
    content = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-4",
                "placeholder": "Content (markdown)",
                "id": "new_content",
            }
        ),
    )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, entry):
    pageContent = util.get_entry(entry);

    return render(request, "encyclopedia/page.html", {
        "title": entry.capitalize(),
        "content": pageContent
    })

def search(request):
    query = request.GET.get("q", "")
    if query is None or query == "":
        return render(
            request,
            "encyclopedia/search.html",
            {"found_entries": "", "query": query},
        )

    matchEntire = util.get_entry(query);
    if matchEntire:
        return redirect("encyclopedia:page", query)

    entries = util.list_entries()

    found_entries = [
        valid_entry
        for valid_entry in entries
        if query.lower() in valid_entry.lower()
    ]

    return render(
        request,
        "encyclopedia/search.html",
        {"found_entries": found_entries, "query": query},
    )


def new(request):
    if request.method == "GET":
        return render(
            request, "encyclopedia/new.html", {"form": NewEntryForm()}
        )

    form = NewEntryForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        content = form.cleaned_data.get("content")

        if title.lower() in [entry.lower() for entry in util.list_entries()]:
            messages.add_message(
                request,
                messages.WARNING,
                message=f'Entry "{title}" already exists',
            )
        else:
            with open(f"entries/{title}.md", "w") as file:
                file.write(content)
            return redirect("encyclopedia:page", title)

    else:
        messages.add_message(
            request, messages.WARNING, message="Invalid request form"
        )

    return render(
        request,
        "encyclopedia/new.html",
        {"form": form},
    )


def random_entry(request):
    entries = util.list_entries()
    entry = entries[randint(0, len(entries) - 1)]
    return redirect("encyclopedia:page", entry)


def edit(request, entry):
    if request.method == "GET":
        title = entry
        content = util.get_entry(title)
        form = NewEntryForm({"title": title, "content": content})
        return render(
            request,
            "encyclopedia/edit.html",
            {"form": form, "title": title},
        )

    form = NewEntryForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        content = form.cleaned_data.get("content")

        util.save_entry(title=title, content=content)
        return redirect("encyclopedia:page", title)

