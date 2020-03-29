
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import loader
from.models import Question, Choice
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'


def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    context ={
        "pagetitle" : 'Vote'
        }
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'polls/detail.html' ,
        {
            'question': question,
            'error_message' : "You did not select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # ALWAYS return HTTPRESPONSEREDIRECT after POST data. Prevent twice submission
        return HttpResponseRedirect(reverse('polls:results',args=(question.id)))
