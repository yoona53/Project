from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Word
from django.db.models import Q
import random, json, re


def home(request):
    return render(request, 'wordle/home.html')

def study(request):
    return render(request, 'wordle/study.html')

MAX_ATTEMPTS = 6

def is_hiragana_only(text):
    return all('ぁ' <= ch <= 'ん' or ch == 'ー' for ch in text)

def compare_words(answer, guess):
    result = []
    for i, ch in enumerate(guess):
        if i < len(answer) and ch == answer[i]:
            result.append('green')
        elif ch in answer:
            result.append('yellow')
        else:
            result.append('gray')
    return result

def quiz(request):
    level = request.GET.get('level', 'all')

    # クイズリセット (GET ?reset=1)
    if request.GET.get("reset") == "1":
        for key in ['answer', 'expression', 'attempts', 'level']:
            request.session.pop(key, None)
        request.session['level'] = level
        return redirect(f"{request.path}?level={level or request.session.get('level', 'all')}")


    # 新しい問題（リセット）
    if 'answer' not in request.session or request.session.get('level') != level:
        qs = Word.objects.filter(active=True)

        # level から数字を抽出
        match = re.search(r'\d+', level)
        if match:
            number = match.group()
            qs = qs.filter(tags__icontains=number)

        word = qs.order_by('?').first()

        if not word:
            return render(request, 'wordle/quiz.html', {'error': f'{level} の単語が見つかりません。'})
        
        # session save
        request.session['answer'] = word.reading
        request.session['expression'] = word.expression
        request.session['attempts'] = []
        request.session['level'] = level

    answer = request.session.get('answer')
    expression = request.session.get('expression')
    attempts = request.session.get('attempts', [])
    error = None
    print("한자: " + expression)
    print("정답: " + answer)

    if request.method == 'POST':
        guess = request.POST.get('guess', '').strip()

        if not is_hiragana_only(guess):
            error = "ひらがなで入力してください。"
        elif len(guess) != len(answer):
            error = f"{len(answer)}文字のひらがなを入力してください。"
        elif len(attempts) >= MAX_ATTEMPTS:
            error = "もう試行回数を使い切りました。"
        else:
            colors = compare_words(answer, guess)
            attempts.append(list(zip(guess, colors)))
            request.session['attempts'] = attempts

            if guess == answer:
                context = {
                    'correct': True,
                    'expression': expression,
                    'answer': answer,
                    'attempts': attempts,
                    'level': level,
                }
                for key in ['answer', 'expression', 'attempts']:
                    request.session.pop(key, None)
                return render(request, 'wordle/result.html', context)

            elif len(attempts) >= MAX_ATTEMPTS:
                context = {
                    'correct': False,
                    'expression': expression,
                    'answer': answer,
                    'attempts': attempts,
                    'level': level,
                }
                for key in ['answer', 'expression', 'attempts']:
                    request.session.pop(key, None)
                return render(request, 'wordle/result.html', context)

    return render(request, 'wordle/quiz.html', {
        'expression': expression,
        'answer': answer,
        'attempts': attempts,
        'attempts_json': json.dumps(attempts, ensure_ascii=False),
        'remaining': MAX_ATTEMPTS - len(attempts),
        'error': error,
        'level': level,
    })

def study(request):
    view_mode = request.GET.get('view', 'list')
    level = request.GET.get('level', 'all')
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))

    words = Word.objects.filter(active=True)

    match = re.search(r'\d+', level)
    
    if match:
        number = match.group()
        words = words.filter(tags__icontains=number)

    if query:
        words = words.filter(Q(expression__icontains=query) | Q(reading__icontains=query))

    if view_mode == 'card':
        paginator = Paginator(words.order_by('expression'), 1)
    else:
        paginator = Paginator(words.order_by('expression'), 20)

    page_obj = paginator.get_page(page)

    context = {
        'view_mode': view_mode,
        'page_obj': page_obj,
        'level': level,
        'query': query,
    }

    return render(request, 'wordle/study.html', context)
