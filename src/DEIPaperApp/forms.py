from django import forms

class NewPaperForm (forms.Form):
    title = forms.CharField(label = "Title")
    abstract = forms.CharField(label = "Abstract")
    authors = forms.CharField(label = "Authors")
    logo_url = forms.URLField(label = "Logo URL", required = False)
    doc_url = forms.URLField(label = "Document URL", required = False)

    def create_json(self):
        return {"title": self.cleaned_data["title"],
                "abstract": self.cleaned_data["abstract"],
                "authors": self.cleaned_data["authors"],
                "logoUrl": self.cleaned_data["logo_url"],
                "docUrl": self.cleaned_data["doc_url"]}

class UpdateAmountForm (forms.Form):
    amount_in_stock = forms.IntegerField(label="New amount in stock:")

    def update_json(self, bev):
        bev["amountInStock"] = self.cleaned_data["amount_in_stock"]
        return bev