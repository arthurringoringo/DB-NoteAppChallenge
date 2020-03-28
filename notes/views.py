from django.shortcuts import render,redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from .models import Note
from django.urls import reverse
from django.views import generic
from .forms import CreateForm
# Create your views here.

class NoteList(generic.ListView):
    template_name = 'notes/notes.html'
    context_object_name = 'NoteList'
    model = Note

class NoteView(generic.DetailView):
    template_name = 'notes/noteview.html'
    model = Note

def NoteCreate(request,template_name='notes/noteCreate.html'): 
    form = CreateForm()
    
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/notes/')
    context= {'form':form}
    return render(request, 'notes/noteCreate.html',context)
    
