from ast import Try
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from . import papers, forms

def list_papers(request: HttpRequest, offset = 0, lines = 10) -> HttpResponse:
    """Show a page with a list containing a
    maximum of the given amount of papers."""
    size_options = (50, 20, 10, 5)
    if lines not in size_options:
        # Restrict size options to those explicitly provided
        return redirect(f"/DEIPaper/papers/offset={offset}&lines=10")
    try:
        page = (offset // lines) + 1
        paper_list = papers.get_papers(lines * (page - 1), lines + 1)    
        papers_len = len(paper_list)
        if papers_len == 0:
            # Redirect to offset 0 if for some reason the returned paper list
            # was empty (for example, if the query was manually changed)
            return redirect(f"/DEIPaper/papers/offset=0&lines={lines}") 
        pages = range(1, min(page, 5))
        paper_list = paper_list[:min(lines, papers_len)]
        has_next_page = papers_len > lines
        has_prev_page = page > 1
        
        # TO-DO: - Position properly pagination buttons
        #        - Set maximum size for each column
        return render(request,
                      "DEIPaperApp/list.html",
                      {"paper_list": paper_list,
                       "page": page,
                       "pages": pages,
                       "lines": lines,
                       "offset": offset,
                       "has_next_page": has_next_page,
                       "has_prev_page": has_prev_page,
                       "size_options": size_options})
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

def show_paper(request: HttpRequest, paper_id: int) -> HttpResponse:
    """Show a paper from the
    ISTPaper system given its ID."""
    try:
        paper = papers.get_paper(paper_id)
        return render(request, "DEIPaperApp/paper.html", {"paper": paper})
    except papers.DEIPaperError as e:
        return e.show_error(request)

def update_paper(request: HttpRequest, paper_id) -> HttpResponse:
    """Update paper from the
    ISTPaper system given its ID."""
    if request.method == "POST":
        form = forms.UpdatePaperForm(request.POST)
        if form.is_valid():
            try:
                paper = papers.get_paper(paper_id) # This might be unnecessary...
                form.update_json(paper)
                papers.update_paper(paper_id, paper)
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