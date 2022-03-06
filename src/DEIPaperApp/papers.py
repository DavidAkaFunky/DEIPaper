from django.http import HttpRequest, HttpResponse
from json import JSONDecodeError
from . import views
import requests

API_URL = "https://aduck.rnl.tecnico.ulisboa.pt/istpaper/papers/"
API_AUTH = "Bearer ist195550" # This should be hidden in production, for obvious reasons

GET_PAPERS_FAIL = "There was a problem fetching the papers list."
POST_PAPER_FAIL = "There was a problem adding the new paper to the system."
DEL_PAPER_FAIL = "There was a problem removing the paper from the system."
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
    raise DEIPaperError(r.status_code, GET_PAPERS_FAIL, errors)

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
    raise DEIPaperError(r.status_code, POST_PAPER_FAIL, errors)

def delete_paper(paper_id) -> None:
    errors = {400: INV_PAPER_ID, 401: INV_ACC_TOKEN, 403: NO_PERM, 404: PAPER_NOT_FOUND}
    r = requests.delete(API_URL + str(paper_id),
                        headers = {"Authorization": API_AUTH})
    if not r.ok:
        raise DEIPaperError(r.status_code, DEL_PAPER_FAIL, errors)

class DEIPaperError(Exception):
    def __init__ (self, code: int, msg_comm: str, msg_dict: dict) -> None:
        self.code = code
        self.msg = [msg_comm]
        try:
            self.msg.append(msg_dict[code])
        except KeyError:
            self.msg.append(UNEXPECTED_ERROR)

    def get_code(self) -> int:
        return self.code

    def get_msgs(self) -> list:
        return self.msg