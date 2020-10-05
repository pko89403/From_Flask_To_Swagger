from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, Http404
from .models import *

from django.views import generic


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
    template_name = 'polls/results.html'



# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    context = {'latest_question_list' : latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    #try:
    #    q = Question.objects.get(pk = question_id)
    #except Question.DoesNotExist:
    #    raise Http404("Question %s does not exist" % question_id )
    q = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/details.html', {'question' : q})
    

def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except:
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('polls:results', pk = question.id)

    return HttpResponse("You're voting on question %s" % question_id)