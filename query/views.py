from django.shortcuts import render, redirect
from .query import get_data_wikidata, get_image_external, search, literal_details, character_details, episode_details, character_details_portrayer, episode_casting, char_to_episode

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
        'lit': literal_details(data),
        'char': character_details(data),
        'eps': episode_details(data),
        'charportray': character_details_portrayer(data),
        'epscast': episode_casting(data),
        'epslist': char_to_episode(data),
        'extra': get_data_wikidata(data),
    }
    context["urlImage"] = get_image_external(
        next((item["result"] for item in context['lit'] if item["label"] == "Wiki URL"), None)
    )
    return render(request, "detail/detail.html", context=context)