from django.shortcuts import render, redirect
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
    return render(request, 'index/index.html')


def result(request):
    query = request.GET.get('query', '') 
    context = {
        'query': query
    }
    return render(request, 'result/result.html', context=context)

