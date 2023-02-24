import json
import os
import subprocess
from datetime import time

import pydub
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import moviepy.editor as mpe
import xml.etree.ElementTree as ET

from moviepy.audio.AudioClip import concatenate_audioclips
from pydub import AudioSegment

from abridgedworld import settings
from .forms import Video_form
from .models import Videos, Character, Snippet, SnippetSound

# Create your views here.


def home(request):
    '''deals with requests to the home page'''
    return render(request, 'home.html')


def upload_video(request):
    if request.method == 'POST':
        title = request.POST['title']
        video = request.FILES
        form = Video_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponse("<h1> Uploaded successfully </h1>")
        # content = Videos(title=title, video=video)
        # content.save()
        # return display(request)
    videos = Videos.objects.all()
    context = {
        'videos': videos,
    }
    return render(request, 'upload.html', context)

def upload_Voiceover(request, GameName="", SnippetName=""):
    if request.method == 'POST':
        blob = request.FILES["audio_data"]

        audio_path = default_storage.save('audio/' + '123' + '.wav', ContentFile(blob.read()))
        path = os.getcwd()
        print("Current Directory", path)
        # prints parent directory
        #path = os.path.abspath(os.path.join(path, os.pardir))
        path = path.replace('\\', '/')
        audio_path = audio_path.replace('\\', '/')
        media_path = f"{path}/media/"
        cmd = f"""ffmpeg -threads 2 -y -t 2 -i "{media_path}{audio_path}" "{media_path}/audio/{GameName}{SnippetName}.mp3"""
        returned_value = subprocess.call(cmd, shell=True)
        #snippetsounds = SnippetSound.objects.filter(game_name=GameName).filter(snippet_id=SnippetName)[0]
        #snippetsounds.delete()
        new_sound = SnippetSound(game_name=GameName, snippet_id=SnippetName, file_url=f"/media/audio/{GameName}{SnippetName}.mp3")
        new_sound.save()
        return HttpResponse("<h1> Uploaded successfully </h1>")

    videos = Videos.objects.all()
    context = {
        'videos': videos,
    }
    return render(request, 'videos.html', context)

def display(request):
    videos = Videos.objects.all()
    context = {
        'videos': videos,
    }

    return render(request, 'videos.html', context)


# anything to do with characters shall go down here
def upload_character(request):
    if request.method == 'POST':
        name = request.POST['name']
        title = request.POST['title']
        video = Videos.objects.filter(title=title)
        characters = []
        dict_of_characters = Character.objects.filter(video__title=title).values('name')
        for names in dict_of_characters:
            characters.append(names.get("name"))

        if name in characters:
            return HttpResponse("<h1> Character already exists </h1>")
        else:
            character = Character(name=name, video=video[0])
            character.save()
    videos = Videos.objects.all()
    context = {
        'videos': videos,
    }
    return render(request, 'upload.html', context)


def get_characters(request):
    video_title = request.GET.get('video_title', "")
    characters = list(Character.objects.filter(video__title=video_title).values('name'))

    response = {
        'characters': characters or ""
    }
    return JsonResponse(response)


def make_snippet(request):
    if request.method == 'POST':
        video_title = request.POST['video_title']
        character_name = request.POST['character']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        main_video = Videos.objects.filter(title=video_title)[0]
        character = Character.objects.filter(video__title=video_title).filter(name=character_name)
        main_video_url = main_video.video
        directory_path = os.getcwd()
        video = mpe.VideoFileClip(f"{directory_path}{settings.MEDIA_URL}{main_video_url}")
        clip = video.subclip(start_time, end_time)
        clip.write_videofile(f'{directory_path}{settings.MEDIA_URL}/videos/{video_title}{start_time}{end_time}.mp4')
        new_snippet = Snippet(video=main_video, snippet=f'{video_title}{start_time}{end_time}.mp4', Character=character[0],
                              start_time=start_time, end_time=end_time)
        new_snippet.save()
        videos = Videos.objects.all()
        context = {
            'videos': videos,
        }
        return render(request, 'upload.html', context)

    return HttpResponse("<h1> Uploaded failed :( </h1>")

def get_snippets(request):
    video_title = request.GET.get('video_title', "")
    snippets = list(Snippet.objects.filter(video__title=video_title).values('snippet'))

    response = {
        'snippets': snippets or ""
    }
    return JsonResponse(response)

def View_games(request):
    videos = Videos.objects.all()
    context = {
        'videos': videos,
    }
    return render(request, 'gameMenu.html', context)

def get_games(request):
    with open(f"{os.getcwd()}/games.json") as json_file:
        data = json.load(json_file)
        #print(data)
    return JsonResponse(data)

def get_snippet_sound(request):
    snippet_id = request.GET.get('snippet-id', "")
    snippetsound = SnippetSound.objects.filter(snippet_id=snippet_id)[0]

    response = {
        'soundurl': snippetsound.file_url or ""
    }
    return JsonResponse(response)

def Game_page(request, name=''):
    with open(f"{os.getcwd()}/games.json") as json_file:
        games = json.load(json_file)
    counter = 0
    for key in games:
        print(games[key])
        for game in games[key]:
            game_name = game.get('name')
            if game_name == name:
                print("match found")
                video_title = game.get('video_title')
        counter = counter + 1

    qvideo = Videos.objects.filter(title=video_title)
    if len(qvideo) > 0:
        video = qvideo[0]
        snippets = Snippet.objects.filter(video__title=video_title)


    else:
        return render(request, 'gameMenu.html')
    context = {
                  'video': video,
                  'snippets': snippets,
                  'gameName' : name,
    }
    #print(context)
    return render(request, 'GamePage.html', context)


def RecordSnippet(request, GameName="", SnippetName=""):
    snippets = ""
    try:
        with open(f"{os.getcwd()}/games.json") as json_file:
            games = json.load(json_file)
        for key in games:
            print(games[key])
            for game in games[key]:
                game_name = game.get('name')
                if game_name == GameName:
                    print("match found")
                    video_title = game.get('video_title')

        qvideo = Videos.objects.filter(title=video_title)
        if len(qvideo) > 0:
            snippet = Snippet.objects.filter(video__title=video_title).filter(id=SnippetName)[0]

    finally:
        context = {
            'snippet': snippet,
            'game_name': game_name
        }
        return render(request, 'RecordSnippet.html', context)

def make_new_game(request):
    if request.method == 'POST':
        game_name = request.POST['Game_name']
        video_title = request.POST['video_title']
        video = Videos.objects.filter(title=video_title)[0]

        with open(f"{os.getcwd()}/games.json") as json_file:
            data = json.load(json_file)
        data['games'].append({
            "name": game_name,
            "players": {},
            "Limit": video.players,
            "video_title": video_title
        })
        with open(f"{os.getcwd()}/games.json", 'w') as outfile:
            json.dump(data, outfile)
    videos = Videos.objects.all()
    context = {
        'videos': videos,
    }
    return render(request, 'gameMenu.html', context)


def build_video(request):
    game_name = request.GET.get('Game_name', "")
    video_title = request.GET.get('video_title', "")
    snippetsounds = SnippetSound.objects.filter(game_name=game_name)
    video = Videos.objects.filter(title=video_title)[0]
    print(f"ggggggggg {snippetsounds.count()}")
    cwd = os.getcwd().replace('\\', '/')
    combined_sounds = []
    for index in range(int(snippetsounds.count())):
        combined_sounds.append(mpe.AudioFileClip(f"{cwd}/{snippetsounds[index].file_url}"))


    if len(combined_sounds) > 0:
        concat = concatenate_audioclips(combined_sounds)
        concat.write_audiofile(f"{cwd}/media/sound.mp3")
        my_clip = mpe.VideoFileClip(f"{cwd}{video.video.url}")
        final_clip = my_clip.set_audio(concat)
        final_clip.write_videofile(f"{cwd}/media/videos/{game_name}.mp4")

    context = {
        'finishedVideo': f"/media/videos/{game_name}.mp4"
    }
    return JsonResponse(context)