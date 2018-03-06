from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #необходимо для переключения между страницами

from .models import Choice, Question



def index(request,):
    question_list = Question.objects.all()
    paginator = Paginator(question_list, 10) #Отображает 10 вопросов на странице
    
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    
    return render_to_response('polls/index.html', {"questions": questions})



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        #request.POST вызывает исключение KeyError, если такого ключа нет в наборе существующих
        #использую POST, а не GET, так как отправка формы изменяет данные.Иначе использовал бы GET
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
        #Обрабатывает KeyError и возвращает ошибку,если не выбран ни один вариант ответа
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        #HttpResponseRedirect перенаправляет пользователя в результаты голосованя



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
