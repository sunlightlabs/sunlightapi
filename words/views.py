import string 
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseForbidden
from sunlightapi.api.models import ApiKey
from sunlightapi.words.models import WordList
from django.shortcuts import get_object_or_404
from django.utils.functional import wraps

MAX_WORDLIST_BYTES = 5000

def with_apiuser(func):
    def wrapper(request, *args, **kwargs):
        # get the user who is calling the service
        try:
            apikey = request.REQUEST['apikey']
            apiuser = ApiKey.objects.get(key=apikey, status='A')
        except KeyError:
            return HttpResponseForbidden('Missing API Key')
        except ObjectDoesNotExist:
            return HttpResponseForbidden('Invalid API Key')

        return func(request, apiuser=apiuser, *args, **kwargs)
    wrapper = wraps(func)(wrapper)
    return wrapper

@with_apiuser
def word_list(request, apiuser, list_name):

    # if method is GET, return a simple listing
    if request.method == 'GET':
        wordlist = get_object_or_404(WordList, slug=list_name)

    # if method is POST, attempt to create/update a list
    elif request.method == 'POST':
        delimiter = request.POST.get('delimiter', '\n')
        words = request.POST['words']

        if len(words) > MAX_WORDLIST_BYTES:
            return HttpResponseForbidden('wordlist exceeds %s character limit'
                                         % MAX_WORDLIST_BYTES)

        # check permissions before updating
        try:
            wordlist = WordList.objects.get(slug=list_name)
            if wordlist.user == apiuser:
                wordlist.delimiter = delimiter
                wordlist.words = words
                wordlist.save()
            else:
                return HttpResponseForbidden('Attempt to modify wordlist that belongs to another user')

        # create if no list with this name exists
        except ObjectDoesNotExist:
            wordlist = WordList.objects.create(slug=list_name, user=apiuser,
                                               words=words, 
                                               delimiter=delimiter)

    return HttpResponse('~'.join(wordlist.word_list), mimetype='text/plain')

@with_apiuser
def remove_stopwords(request, apiuser, list_name):

    # converting to a set yielded great results
    wordlist = set(get_object_or_404(WordList, slug=list_name).word_list)

    text = str(request.POST['text'])
    text = string.translate(text, string.maketrans('',''), string.punctuation)
    text = ' '.join([w for w in text.lower().split() if w not in wordlist])

    return HttpResponse(text, mimetype='text/plain')

