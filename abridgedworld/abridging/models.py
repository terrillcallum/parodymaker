from django.db import models

# Create your models here.


class Videos(models.Model):
    title = models.CharField(max_length=100, unique=True)
    video = models.FileField(upload_to='videos', null=True, verbose_name="")
    players = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'

    def __str__(self):
        return self.title

class Character(models.Model):
    '''this is one of the characters from the video'''
    name = models.TextField(max_length=200)
    video = models.ForeignKey(Videos, default=0, on_delete=models.SET_DEFAULT)

class Snippet(models.Model):
    '''a snippet of one of the videos'''
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    snippet = models.FileField(upload_to='videos/')
    Character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)
    start_time = models.FloatField()
    end_time = models.FloatField()

class SnippetSound(models.Model):
    """
    this is the model that handles a voice being saved this combined then attached with a video to generate a abridged video
    """
    game_name = models.TextField(max_length=100)
    snippet_id = models.TextField(max_length=100)
    file_url = models.TextField(max_length=200)