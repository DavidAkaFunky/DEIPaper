from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from json import JSONDecodeError
import requests

API_URL = "https://aduck.rnl.tecnico.ulisboa.pt/istpaper/papers/"
API_AUTH = "Bearer ist195550" # This should be hidden in production, for obvious reasons

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
    errors = {400: INV_PAPER, 404: INV_PAPER_ID}
    r = requests.get(API_URL + str(paper_id))
    if r.ok:
        try:
            return r.json()
        except JSONDecodeError:
            pass
    raise DEIPaperError(r.status_code, GET_PAPER_FAIL, msg_dict = errors)

def post_paper(paper: dict) -> int:
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
    errors = {400: INV_PAPER_ID, 401: INV_ACC_TOKEN, 403: NO_PERM, 404: PAPER_NOT_FOUND}
    r = requests.delete(API_URL + str(paper_id),
                        headers = {"Authorization": API_AUTH})
    if not r.ok:
        raise DEIPaperError(r.status_code, DEL_PAPER_FAIL, msg_dict = errors)

def update_paper(paper_id: int, paper: dict) -> None:
    errors = {400: INV_PAPER, 403: NO_PERM, 404: PAPER_NOT_FOUND}
    r = requests.put(API_URL + str(paper_id),
                     headers = {"Authorization": API_AUTH},
                     json = paper)
    print("Status code:", r.status_code)
    if not r.ok:
        raise DEIPaperError(r.status_code, UPD_PAPER_FAIL, msg_dict = errors)

class DEIPaperError(Exception):
    def __init__ (self, code: int, title: str, msg_dict: dict) -> None:
        self.code = code
        self.title = title
        try:
            self.msg = msg_dict[code]
        except KeyError:
            self.msg = UNEXPECTED_ERROR

    def show_error(self, request: HttpRequest, redirect_flag = True) -> HttpResponse:
        messages.error(request, f"{self.title} Error {self.code}: {self.msg}")
        if redirect_flag:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))