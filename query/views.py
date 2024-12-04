from django.shortcuts import render, redirect
from .query import search, details

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


def detail(request):
    data = request.GET.get('data', '') 

    if (data == None) or (data == ''):
        return render(request, 'index/index.html')

    context = {
        'data': data,
        'results': details(data)
    }
    return render(request, 'detail/detail.html', context=context)

