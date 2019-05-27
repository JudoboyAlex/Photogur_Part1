from django.http import HttpResponse
from django.shortcuts import render
from photogur.models import Picture, Comment


def pictures_page(request):
    context = {'pictures': Picture.objects.all()}
    response = render(request, 'index.html', context)
    return HttpResponse(response)

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {'picture': picture}
    response = render(request, 'picture.html', context)
    return HttpResponse(response)



# def contacts_list(request):
#     context = {'contacts': Contact.objects.all()}
#     html = render(request, 'index.html', context)
#     return HttpResponse(html)