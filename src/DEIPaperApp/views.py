from django.urls import reverse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from . import papers, forms

def list_papers(request: HttpRequest, page = 1, lines = 10, **kwargs):
    """Show a page with a list containing a
    maximum of the given amount of papers"""
    for key in kwargs:
        header[key] = kw
    try:
        paper_list = papers.get_papers(lines * (page - 1), lines + 1)    
        papers_len = len(paper_list)
        paper_list = paper_list[:min(lines, papers_len)]
        has_next_page = papers_len > lines
        has_prev_page = page > 1
        # TO-DO: The HTML file still doesn't support pagination
        header = {"paper_list": paper_list,
                  "page": page,
                  "has_next_page": has_next_page,
                  "has_prev_page": has_prev_page,
                  "size_options": (5, 10, 20, 50)}
    except papers.DEIPaperError as e:
        msgs = e.get_msgs()
        header["error"] = {"msg1": msgs[0],
                           "code": e.get_code(),
                           "msg2": msgs[1]}
    return render(request, "DEIPaperApp/list.html", header)

def new_paper(request: HttpRequest) -> HttpResponse:
    """Show a page allowing an authenticated user
    to add a new paper to the ISTPaper system"""
    if request.method == "POST":
        form = forms.NewPaperForm(request.POST)
        if form.is_valid():
            try:
                paper_id = papers.post_paper(form.create_json())
                return list_papers(request,
                                   add_success = True) # TO-DO: paper_id needs to be added
            except papers.DEIPaperError as e:
                msgs = e.get_msgs()
                HttpResponseRedirect(reverse("list_papers-main",
                                             kwargs = {"error": {"msg1": msgs[0],
                                                                 "code": e.get_code(),
                                                                 "msg2": msgs[1]}}))
    else:
        form = forms.NewPaperForm()

    return render(request, "DEIPaperApp/papers/new.html", {"form": form})

def show_paper(request, paper_id):
    pass

def update_paper(request, paper_id):
    pass

def delete_paper(request, paper_id):
    try:
        papers.delete_paper(paper_id)
        return HttpResponseRedirect(reverse("list_papers-main",
                                            kwargs = {"del_success": True}))
        
    except papers.DEIPaperError as e:
        msgs = e.get_msgs()
        return HttpResponseRedirect(reverse("list_papers-main",
                                            kwargs = {"error": {"msg1": msgs[0],
                                                                "code": e.get_code(),
                                                                "msg2": msgs[1]}}))