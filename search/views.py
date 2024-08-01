from haystack.query import SearchQuerySet
from django.shortcuts import render

def search_view(request):
    query = request.GET.get('q', '')
    search_results = SearchQuerySet().filter(content=query)
    return render(request, 'search_results.html', {'products': search_results})
