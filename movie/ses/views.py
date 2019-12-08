from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def hello_world(request):
    if request.method == 'POST':
        searchterm = request.form['searchterm']
        # results = ranker.scorer(filename='dataset_cleaned.csv', search_term=searchterm)
    else:
        searchterm = ''
    return render(request, 'hello.html', {})