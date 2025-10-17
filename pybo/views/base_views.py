from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from django.db.models import Q, Count

from ..models import Question, Answer

def index(request):
    """
    pybo 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어
    so = request.GET.get('so', 'recent') # 정렬 기준
    
    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:   # recent
        question_list = Question.objects.order_by("-create_date")
    
    # 조회
    # question_list = Question.objects.order_by("-create_date")
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    
    context = {"question_list" : page_obj, 'page': page, 'kw': kw, 'so':so}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)

    # 입력 인자
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어
    so = request.GET.get('so', 'recent') # 정렬 기준
    
    # 정렬
    if so == 'recommend':
        answer_list = Answer.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'old':
        answer_list = Answer.objects.order_by("create_date")
    else:   # recent
        answer_list = Answer.objects.order_by("-create_date")
    
    # 조회
    # question_list = Question.objects.order_by("-create_date")
    if kw:
        answer_list = answer_list.filter(
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw)
        ).distinct()

    # 페이징 처리
    paginator = Paginator(answer_list, 3)
    page_obj = paginator.get_page(page)
    
    context = {'question' : question, "answer_list" : page_obj, 'page': page, 'kw': kw, 'so':so}
    print(context)
    return render(request, 'pybo/question_detail.html', context)