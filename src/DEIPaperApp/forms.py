from django import forms

class NewPaperForm (forms.Form):
    title = forms.CharField(label = "Title")
    abstract = forms.CharField(label = "Abstract")
    authors = forms.CharField(label = "Authors")
    logoUrl = forms.URLField(label = "Logo URL", required = False)
    docUrl = forms.URLField(label = "Document URL", required = False)

    def create_json(self):
        return {"title": self.cleaned_data["title"],
                "abstract": self.cleaned_data["abstract"],
                "authors": self.cleaned_data["authors"],
                "logoUrl": self.cleaned_data["logoUrl"],
                "docUrl": self.cleaned_data["docUrl"]}

class UpdatePaperForm (forms.Form):
    title = forms.CharField(label = "Title", required = False)
    abstract = forms.CharField(label = "Abstract", required = False)
    authors = forms.CharField(label = "Authors", required = False)
    logoUrl = forms.URLField(label = "Logo URL", required = False)
    docUrl = forms.URLField(label = "Document URL", required = False)

    def update_json(self, paper):
        new_data = self.cleaned_data
        for key in new_data:
            paper[key] = new_data[key]
        return paper