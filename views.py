from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

import random

from .models import Quote
from .forms import *


def index(request):
    context = {}

    if not request.session.get('has_session'):
        request.session['has_session'] = True

    if request.method == 'GET':
        quote = random_quote_text()
        context['likeform'] = LikeForm(
            sessionkey=request.session.session_key,
            quote_id=quote.id
        )
        context['quote'] = quote
        return render(request, 'index.html', context)

    elif request.method == 'POST':
        quote_id = int(request.POST['quote_id_field'])
        form = LikeForm(request.session.session_key, quote_id, request.POST)
        if form.is_valid():
            form.save()
            data = {
                'liked': form.like.liked,
                'likes': form.quote.likes,
            }
            return JsonResponse(data)


def add(request):
    context = {}

    if not request.session.get('has_session'):
        request.session['has_session'] = True

    if request.method == 'POST':
        form = QuoteForm(request.session.session_key, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your oneliner has been submited for approval")
            return HttpResponseRedirect(reverse('oneliners:index'))
    else:
        form = QuoteForm(sessionkey=request.session.session_key)
    context["form"] = form
    return render(request, 'add.html', context)


def random_quote_text():
    quotes = Quote.objects.filter(valid=True)
    quote = random.choice(quotes)
    return quote
