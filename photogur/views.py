from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from photogur.models import Picture, Comment
from django.views.decorators.http import require_http_methods
from photogur.forms import LoginForm, PictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

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

# def login_view(request):
#     form = LoginForm()
#     context = {'form': form}
#     http_response = render(request, 'login.html', context)
#     return HttpResponse(http_response)
  
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pictures')


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/pictures')
    else:
        form = UserCreationForm()
    html_response =  render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)

@login_required
def submit_picture(request):
    if request.method == 'POST':
        form = PictureForm(request.POST)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.user = request.user
            picture.save()
            return redirect("picture_details", id=picture.id)
            # return HttpResponseRedirect('/addpic')
            
    else:
        form = PictureForm()
        context = { 'form': form }
        response = render(request, 'addpicture.html', context)
        return HttpResponse(response)

@login_required
def edit_picture(request, id):
    obj = get_object_or_404(Picture, id = id, user=request.user.id)
    if request.method == "POST":
        form = PictureForm(request.POST, instance= obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('picture_details', id=obj.id)
    else:
        form = PictureForm(instance=obj)
    return render(request, 'edit_picture.html', {'form':form})
  