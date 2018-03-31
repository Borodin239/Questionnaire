from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #необходимо для переключения между страницами
from django.contrib import auth

from .models import Choice, Question



def index(request,):
    username = auth.get_user(request).username
    
    if request.user.is_authenticated():
        question_list = Question.objects.all()
        paginator = Paginator(question_list, 8) #Отображает 8 вопросов на странице
    
        page = request.GET.get('page')
        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
                questions = paginator.page(paginator.num_pages)
    
        return render_to_response('polls/index.html', {"questions": questions, "username": username})

    else :
        return HttpResponseRedirect("/auth/logout")



def detail(request, question_id):
    username = auth.get_user(request).username
    
    if request.user.is_authenticated():
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/detail.html', {'question': question, 'username': username})

    else:
        return HttpResponseRedirect("/auth/logout")

def vote(request, question_id):
    username = auth.get_user(request).username
    
    if request.user.is_authenticated():
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

    else:
        return HttpResponseRedirect("/auth/logout")


def results(request, question_id):
    username = auth.get_user(request).username
    
    if request.user.is_authenticated():
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/results.html', {'question': question, 'username': username})

    else:
        return HttpResponseRedirect("/auth/logout")
