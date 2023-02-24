"""abridgedworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from abridging.views import upload_video, display, home, get_characters, upload_character, make_snippet, get_snippets, \
    View_games, get_games, Game_page, make_new_game, RecordSnippet, upload_Voiceover, get_snippet_sound, build_video

from abridgedworld import settings

urlpatterns = [
    path('', home, name="home"),
    path('upload/', upload_video, name='upload'),
    path('videos/', display, name='videos'),
    path('get_characters/', get_characters, name='get_characters'),
    path('get_snippet_sound/', get_snippet_sound, name='get_snippet_sound'),
    path('View_games/', View_games, name='View_games'),
    path('get_games/', get_games, name='get_games'),
    path('get_snippets/', get_snippets, name='get_snippets'),
    path('upload_character', upload_character, name='upload_character'),
    path('make_snippet', make_snippet, name='make_snippet'),
    path('admin/', admin.site.urls),
    path('Game_page/<name>/', Game_page, name='Game_page'),
    path('RecordSnippet/<GameName>/<SnippetName>/', RecordSnippet, name='RecordSnippet'),
    path('upload_Voiceover/<GameName>/<SnippetName>', upload_Voiceover, name='upload_Voiceover'),
    path('make_new_game', make_new_game, name='make_new_game'),
    path('build_video', build_video, name='build_video')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
