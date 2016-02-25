from django import forms

from .models import *


class LikeForm(forms.Form):
    def __init__(self, sessionkey, quote_id, *args, **kwargs):
        super(LikeForm, self).__init__(*args, **kwargs)
        self.sessionkey = sessionkey
        self.session = get_session(sessionkey)
        self.quote = Quote.objects.get(id=quote_id)
        self.like = get_like(self.quote, self.session)
        if self.like and self.like.liked:
            self.liked = True
        else:
            self.liked = False

        self.fields['quote_id_field'] = forms.IntegerField(
            initial=quote_id,
            widget=forms.NumberInput(
                attrs={'type': 'hidden'}
            )
        )
        self.fields['like_field'] = forms.BooleanField(
            initial=self.liked,
            required=False,
            widget=forms.TextInput(
                attrs={'type': 'hidden'}
            )
        )

    def save(self):
        if not self.session:
            self.session = Session()
            self.session.key = self.sessionkey
            self.session.save()

        if self.like:
            if self.like.liked:
                self.quote.likes -= 1
                self.quote.save()
                self.like.liked = False
            else:
                self.quote.likes += 1
                self.quote.save()
                self.like.liked = True
        else:
            self.quote.likes += 1
            self.quote.save()
            self.like = Like()
            self.like.quote = self.quote
            self.like.session = self.session
            self.like.liked = True
        self.like.save()


class QuoteForm(forms.Form):
    def __init__(self, sessionkey, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.sessionkey = sessionkey
        self.fields['quote_field'] = forms.CharField(
            max_length=255,
            label='Oneliner here',
            error_messages={
                'required': 'Write something here will you'
            },
            widget=forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '5',
                    'placeholder': "I'll be reading this so please try not to disappoint me..."
                }
            )
        )

        self.fields['context_field'] = forms.CharField(
            max_length=255,
            label='Provide context',
            required=False,
            widget=forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': "Optional"
                }
            )
        )

    def clean_quote_field(self):
        quote_text = self.cleaned_data['quote_field']

        existing_quotes = Quote.objects.filter(text=quote_text)
        if len(existing_quotes) > 0:
            raise forms.ValidationError('Oneliner already exists')

        session = get_session(self.sessionkey)
        session_quotes = Quote.objects.filter(session=session)
        if len(session_quotes) > 20:
            raise forms.ValidationError('Slow down turbo')

        return quote_text

    def save(self):
        session = get_session(self.sessionkey)
        session.key = self.sessionkey
        session.save()

        quote = Quote()
        quote.text = self.cleaned_data['quote_field']
        quote.context = self.cleaned_data['context_field']
        quote.session = session
        quote.save()


def get_session(sessionkey):
    try:
        session = Session.objects.get(key=sessionkey)
    except Session.DoesNotExist:
        session = None
    return session


def get_like(quote, session):
    if session:
        try:
            like = Like.objects.get(quote=quote, session=session)
        except Like.DoesNotExist:
            like = None
    else:
        like = None

    return like
