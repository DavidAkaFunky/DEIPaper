from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from json import JSONDecodeError
from . import views
import requests

API_URL = "https://aduck.rnl.tecnico.ulisboa.pt/istpaper/papers"
API_AUTH = "Bearer ist195550" # This should be hidden in production, for obvious reasons

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
    raise DEIPaperError(r.code, msg_dict = errors)

def post_paper(paper) -> int:
    errors = {400: INV_PAPER, 401: INV_ACC_TOKEN}
    r = requests.post(API_URL,
                      headers = {"Authorization": API_AUTH},
                      json = paper)
    if r.ok:
        try:
            return r.json()["id"] # Return the newly created paper"s id
        except JSONDecodeError:
            pass
    raise DEIPaperError(r.code, msg_dict = errors)

def delete_paper(paper_id) -> None:
    errors = {400: INV_PAPER_ID, 401: INV_ACC_TOKEN, 403: NO_PERM, 404: PAPER_NOT_FOUND}
    r = requests.delete(API_URL + str(paper_id),
                        headers = {"Authorization": API_AUTH})
    if not r.ok:
        raise DEIPaperError(r.code, msg_dict = errors)

class DEIPaperError(Exception):
    def __init__ (self, code: int, msg_dict: dict) -> None:
        self.code = code
        try:
            self.msg = msg_dict[code]
        except KeyError:
            self.msg = UNEXPECTED_ERROR

    def render_error(self, request: HttpRequest, self_redirect = False) -> HttpResponse:
        return redirect(request, views.main_page, self_redirect)