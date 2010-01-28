from django.db import models
from sunlightapi.api.models import ApiKey

class WordList(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    user = models.ForeignKey(ApiKey)
    words = models.TextField()
    delimiter = models.CharField(max_length=1)

    def _get_word_list(self):
        if not hasattr(self, '_word_list'):
            self._word_list = self.words.split(self.delimiter)
        return self._word_list

    word_list = property(_get_word_list)

