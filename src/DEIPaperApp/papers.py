"""This file is dedicated to API requests. Each function makes a request 
to the ISTPaper API, raising a custom error which contains the request error
code and a small description, in case it fails. These errors are caught 
in the views.py file, calling the function that displays their details."""

from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from json import JSONDecodeError
import requests

# Base URL where API requests are sent
API_URL = "https://aduck.rnl.tecnico.ulisboa.pt/istpaper/papers/"

# This should be hidden in production for security-related reasons (using environment variables, for example)
API_AUTH = "Bearer ist195550"

# Error messages
GET_PAPERS_FAIL = "There was a problem fetching the papers list."
GET_PAPER_FAIL = "There was a problem fetching the requested paper."
POST_PAPER_FAIL = "There was a problem adding the new paper to the system."
DEL_PAPER_FAIL = "There was a problem removing the paper from the system."
UPD_PAPER_FAIL = "There was a problem updating the paper in the system."
INV_LIM = "Invalid limit/offset"
INV_ACC_TOKEN = "Access token missing or invalid"
INV_PAPER = "Invalid paper"
INV_PAPER_ID = "Invalid paper ID"
NO_PERM = "No permission to perform requested operation on requested resource"
UNEXPECTED_ERROR = "Unexpected error"
PAPER_NOT_FOUND = "Paper not found"

def get_papers(offset: int, lines: int) -> dict:
    """Make API get request for a list of 'lines' papers, skipping
    the first 'offset' papers (at the moment of the development,
    it still skips the first 'offset' papers instead)."""
    errors = {400: INV_LIM}
    r = requests.get(API_URL, 
                     params = {"offset": offset,
                               "lines": lines})
    if r.ok:
        try:
            return r.json()
        except JSONDecodeError:
            pass
    raise DEIPaperError(r.status_code, GET_PAPERS_FAIL, msg_dict = errors)

def get_paper(paper_id: int) -> dict:
    """Make API get request for a paper given its ID."""
    errors = {400: INV_PAPER, 404: INV_PAPER_ID}
    r = requests.get(API_URL + str(paper_id))
    if r.ok:
        try:
            return r.json()
        except JSONDecodeError:
            pass
    raise DEIPaperError(r.status_code, GET_PAPER_FAIL, msg_dict = errors)

def post_paper(paper: dict) -> int:
    """Make API post request for the addition of a new paper."""
    errors = {400: INV_PAPER, 401: INV_ACC_TOKEN}
    r = requests.post(API_URL,
                      headers = {"Authorization": API_AUTH},
                      json = paper)
    if r.ok:
        try:
            return r.json()["id"] # Return the newly created paper's id
        except JSONDecodeError:
            pass
    raise DEIPaperError(r.status_code, POST_PAPER_FAIL, msg_dict = errors)

def delete_paper(paper_id: int) -> None:
    """Make API delete request to delete a paper given its id."""
    errors = {400: INV_PAPER_ID, 401: INV_ACC_TOKEN, 403: NO_PERM, 404: PAPER_NOT_FOUND}
    r = requests.delete(API_URL + str(paper_id),
                        headers = {"Authorization": API_AUTH})
    if not r.ok:
        raise DEIPaperError(r.status_code, DEL_PAPER_FAIL, msg_dict = errors)

def update_paper(paper_id: int, paper: dict) -> None:
    """Make API put request to update a paper with new
    information (contained in 'paper') given its id."""
    errors = {400: INV_PAPER, 403: NO_PERM, 404: PAPER_NOT_FOUND}
    r = requests.put(API_URL + str(paper_id),
                     headers = {"Authorization": API_AUTH},
                     json = paper)
    if not r.ok:
        raise DEIPaperError(r.status_code, UPD_PAPER_FAIL, msg_dict = errors)

class DEIPaperError(Exception):
    """Custom error, containing the code of the failed
    request and its corresponding error message."""
    def __init__ (self, code: int, title: str, msg_dict: dict) -> None:
        self.code = code
        self.title = title
        try:
            self.msg = msg_dict[code]
        except KeyError:
            self.msg = UNEXPECTED_ERROR

    def show_error(self, request: HttpRequest, redirect_flag = True) -> HttpResponse:
        """Temporarily display an alert
        containing the error's attributes."""
        messages.error(request, f"{self.title} Error {self.code}: {self.msg}")
        if redirect_flag:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))