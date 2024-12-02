from django.shortcuts import render, redirect
from .query import search

# Create your views here.

def index(request):
    return render(request, 'index/index.html')


def result(request):
    query = request.GET.get('query', '') 

    if (query == None) or (query == ''):
        return render(request, 'index/index.html')

    context = {
        'query': query,
        'results': search(query)
    }
    return render(request, 'result/result.html', context=context)

