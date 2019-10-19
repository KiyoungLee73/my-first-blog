from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic


from .models import Question, Choice

def index(request):
    # Case #1
    #return HttpResponse("Hello, world. You're at the poll index.")

    # Case #2
    #lastest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([q.question_text for q in lastest_question_list])
    #return HttpResponse(output)

    # Case #3
    lastest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_tempalte('polls/index.html')
    context = {
        'lastest_question_list': lastest_question_list,
    }
    return render(request, 'polls/index.html', context)



def detail(request, question_id):
    # Case #1
    # return HttpResponse("You're looking at question %s." % question_id)

    # Case #2
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    # return render(request, 'polls/detail.html', {'question':question})

    # Case #3
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})


def results(request, question_id):
    # Case #1
    # response = "You're looking at result of question %s."
    # return HttpResponse(response % question_id)

    # Case #2
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    # Case #1
    # return HttpResponse("You're voting on question %s." % question_id)

    # Case #2
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lastest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
