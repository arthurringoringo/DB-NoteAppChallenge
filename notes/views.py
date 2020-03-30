from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse, HttpResponseRedirect
from .models import Note
from django.urls import reverse
from django.views import generic
from .forms import CreateForm
from datetime import datetime
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
    
def NoteUpdate(request,note_id):
    note = get_object_or_404(Note, pk=note_id)
   
    if request.method == 'POST':
        note.context = request.POST.get('NoteContext')
        note.modify_date = datetime.now()
        note.save()
        return HttpResponseRedirect(reverse('notes:noteview', args=(note.id,)))
        
def NoteDelete(request,note_id):
    note  =  get_object_or_404(Note,pk=note_id)

    if request.method == 'POST':
        note.delete()
        return HttpResponseRedirect(reverse('notes:notelist'))

