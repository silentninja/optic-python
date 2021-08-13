from django import forms
from django.http import HttpResponse, JsonResponse


def view1(request):
    return HttpResponse("view1")


def view2(request):
    return HttpResponse("view2")


def json_view(request):
    return JsonResponse({"foo": "bar"})


class NameForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=100)
    names = forms.MultipleChoiceField(choices=(("foo", "Foo"), ("bar", "Bar")))


def form_view(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse("Created")
