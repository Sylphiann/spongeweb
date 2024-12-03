from django.shortcuts import render
from django.conf import settings
from SPARQLWrapper import SPARQLWrapper, JSON

# Create your views here.

def __query(query: str):
    sparql = SPARQLWrapper(settings.GRAPH_DB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def index(request):
    return render(request, 'index.html')


def search(request):
    pass

