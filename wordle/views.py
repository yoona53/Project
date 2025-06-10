from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Word
import random

def compare_words(answer, guess):
    result = []
    for i in range(len(guess)):
        if i < len(answer) and guess[i] == answer[i]:
            result.append('green')
        elif guess[i] in answer:
            result.append('yellow')
        else:
            result.append('gray')
    return result

def game(request: HttpRequest):
    MAX_ATTEMPTS = 6

    # 1) GET 파라미터로 받은 len_type
    len_type = int(request.GET.get('len', request.session.get('len', 5)))

    # 2) '새 게임 시작 여부' 판단: 
    #    - 세션에 저장된 answer가 없거나
    #    - 이전에 선택했던 길이(request.session['len'])와 다르다면
    if 'answer' not in request.session or request.session.get('len') != len_type:
        # DB에서 길이에 맞는 active 단어를 랜덤으로 하나 꺼내서
        qs = Word.objects.filter(length=len_type, active=True)
        word = qs.order_by('?').first()
        if not word:
            return render(request, 'wordle/game.html', {
                'error': f"{len_type}글자 단어가 없습니다.",
            })
        # 세션 초기화
        request.session['answer'] = word.text
        request.session['len'] = len_type
        request.session['attempts'] = []

    answer   = request.session['answer']
    attempts = request.session.get('attempts', [])
    error    = None

    # 3) POST 요청 처리
    if request.method == 'POST':
        guess = request.POST.get('guess', '').strip()

        # 길이 검증
        if len(guess) != len_type:
            error = f"{len_type}文字の単語を入力してください。"
        # 남은 횟수 초과 검증
        elif len(attempts) >= MAX_ATTEMPTS:
            error = "もう試行回数を使い切りました。"
        else:
            colors = compare_words(answer, guess)
            # (char, color) 튜플 리스트를 시도 기록에 추가
            attempts.append(list(zip(guess, colors)))
            request.session['attempts'] = attempts

            # 정답 맞추면 결과 페이지로
            if guess == answer:
                return render(request, 'wordle/result.html', {
                    'correct': True,
                    'answer': answer,
                })

    # 4) 템플릿에 보낼 컨텍스트
    return render(request, 'wordle/game.html', {
        'attempts': attempts,
        'error': error,
        'remaining': MAX_ATTEMPTS - len(attempts),
        'len': len_type,
    })
