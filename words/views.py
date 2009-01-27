from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseForbidden
from sunlightapi.api.models import ApiUser
from sunlightapi.words.models import WordList
from django.shortcuts import get_object_or_404

def word_list(request, list_name):

    # get the user who is calling the service
    try:
        apikey = request.REQUEST['apikey']
        apiuser = ApiUser.objects.get(api_key=apikey, status='A')
    except KeyError:
        return HttpResponseForbidden('Missing API Key')
    except ObjectDoesNotExist:
        return HttpResponseForbidden('Invalid API Key')

    # if method is GET, return a simple listing
    if request.method == 'GET':
        wordlist = get_object_or_404(WordList, slug=list_name)

    # if method is POST, attempt to create/update a list
    elif request.method == 'POST':
        delimiter = request.POST.get('delimiter', '\n')
        words = request.POST['words']

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


