from ast import Try
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from . import papers, forms

def list_papers(request: HttpRequest, page = 1, lines = 10) -> HttpResponse:
    """Show a page with a list containing a
    maximum of the given amount of papers."""
    try:
        paper_list = papers.get_papers(lines * (page - 1), lines + 1)    
        papers_len = len(paper_list)
        paper_list = paper_list[:min(lines, papers_len)]
        has_next_page = papers_len > lines
        has_prev_page = page > 1
        # TO-DO: The HTML file still doesn't support pagination
        return render(request,
                      "DEIPaperApp/list.html",
                      {"paper_list": paper_list,
                       "page": page,
                       "has_next_page": has_next_page,
                       "has_prev_page": has_prev_page,
                       "size_options": (5, 10, 20, 50)})
    except papers.DEIPaperError as e:
        return e.show_error(request, redirect_flag = False)

def new_paper(request: HttpRequest) -> HttpResponse:
    """Show a page allowing to add
    a new paper to the ISTPaper system."""
    if request.method == "POST":
        form = forms.NewPaperForm(request.POST)
        if form.is_valid():
            try:
                paper_id = papers.post_paper(form.create_json())
                messages.success(request, f"Paper added successfully. Paper ID: {paper_id}")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except papers.DEIPaperError as e:
                return e.show_error(request)
    else:
        form = forms.NewPaperForm()

    return render(request, "DEIPaperApp/new_paper.html", {"form": form})

def show_paper(request, paper_id):
    """Show a paper from the
    ISTPaper system given its ID."""
    try:
        paper = papers.get_paper(paper_id)
        return render(request, "DEIPaperApp/paper.html", {"paper": paper})
    except papers.DEIPaperError as e:
        return e.show_error(request)

def update_paper(request, paper_id):
    """Update paper from the
    ISTPaper system given its ID."""
    if request.method == "PUT":
        form = forms.UpdatePaperForm(request.PUT)
        if form.is_valid():
            try:
                paper = papers.get_paper(paper_id) # This might be unnecessary...
                papers.update_paper(paper_id, form.update_json(paper))
                messages.success(request, f"Paper with the ID {paper_id} updated successfully.")
                return render(request, "DEIPaperApp/paper.html", {"paper": paper})
            except papers.DEIPaperError as e:
                return e.show_error(request)
    else:
        form = forms.UpdatePaperForm()

    try:
        paper = papers.get_paper(paper_id)
        return render(request, "DEIPaperApp/update_paper.html", {"form": form, "paper": paper})
    except papers.DEIPaperError as e:
        return e.show_error(request)

def delete_paper(request, paper_id):
    """Delete paper from the
    ISTPaper system given its ID."""
    try:
        papers.delete_paper(paper_id)
        messages.success(request, f"Paper with ID {paper_id} deleted successfully.")
        return redirect("/")
    except papers.DEIPaperError as e:
        return e.show_error(request)