"""This file is dedicated to the paper addition and update forms."""

from django import forms

class PaperForm (forms.Form):
    title = forms.CharField(label = "Title")
    abstract = forms.CharField(label = "Abstract", widget = forms.Textarea)
    authors = forms.CharField(label = "Authors")
    logoUrl = forms.URLField(label = "Logo URL", required = False)
    docUrl = forms.URLField(label = "Document URL", required = False)

    def create_json(self, paper_id = None):
        json = {"title": self.cleaned_data["title"],
                "abstract": self.cleaned_data["abstract"],
                "authors": self.cleaned_data["authors"],
                "logoUrl": self.cleaned_data["logoUrl"],
                "docUrl": self.cleaned_data["docUrl"]}
        if paper_id != None:
            json["id"] = paper_id
        return json