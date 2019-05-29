from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from photogur.models import Picture, Comment
from django.views.decorators.http import require_http_methods


def pictures_page(request):
    context = {'pictures': Picture.objects.all()}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {'picture': picture}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)

def picture_search(request):
  query = request.GET['query']
  search_results = Picture.objects.filter(artist=query)
  context = {'pictures': search_results, 'query': query}
  response = render(request, 'search.html', context)
  return HttpResponse(response)  


@require_http_methods(['POST'])
def create_comment(request):
  # this is where we'll receive the form submission
    picture = request.POST['picture']
    name = request.POST['name']
    message = request.POST['message']
    commented_picture = Picture.objects.get(pk=request.POST['picture'])
    new_comment = Comment(picture = commented_picture , name = name, message = message)
    new_comment.save()
    return HttpResponseRedirect('/pictures/' + picture)   


