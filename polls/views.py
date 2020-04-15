
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import loader
from.models import Question, Choice
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    """
    Return the last five published question(not including those set to be publisehd in the future)
    """
    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
class ResultsView(generic.DetailView):
    model = Question, Choice
    template_name = 'polls/results.html'
    def get_queryset(self):
        """
        return choices that has a minum of 1 vote
        """
        return Question.objects


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
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

