from .models import Videos, SnippetSound
from django import forms

class Video_form(forms.ModelForm):
    class Meta:
        model=Videos
        fields=("title", "video", "players")

