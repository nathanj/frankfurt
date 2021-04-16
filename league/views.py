import datetime
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .models import Table, Week
from .scheduler import create_matchups


def matches(request):
    print(request)
    week = Week.objects.order_by('-start').first()

    for i in range(20):
        week.start += datetime.timedelta(days=7)
        week = Week(start=week.start)
        week.save()

        matchups = create_matchups()
        for m in matchups:
            Table(week=week, player1=m[0],
                    player1_corp_deck=m[5],
                    player1_runner_deck=m[2],
                    player2=m[1],
                    player2_corp_deck=m[3],
                    player2_runner_deck=m[4]).save()

    return redirect('/')

def index(request):
    week = Week.objects.order_by('-start').first()
    weeks = Week.objects.order_by('-start')
    tables = Table.objects.filter(week=week).select_related().all()
    context = {
        'week': week,
        'weeks': weeks,
        'tables': tables,
    }
    return render(request, 'base.html', context)
