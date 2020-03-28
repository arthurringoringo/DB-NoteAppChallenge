from django.shortcuts import render
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
    form = CreateForm(request.POST)
    
    if form.is_valid():
        title = form.cleaned_data['notetitle']
        notecontext = form.cleaned_data['notecontext']
        try:
            new = Note(note_title=title, context=notecontext)
        except (KeyError):
            pass
        else:
            new.save()
            return HttpResponseRedirect(reverse('notes:noteview', args=new.pk))
    else:
        form=CreateForm()
    
    return render(request,'notes/noteCreate.html')
    
