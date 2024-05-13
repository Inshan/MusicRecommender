from django.shortcuts import render
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from .forms import ArtistForm
from django.contrib.auth.decorators import login_required
from .recommendations import recommendations
import math
import requests


# from sklearn.ensemble import RandomForestClassifier
# import pandas as pd
# import platform


def getsphandle():
    TIMEOUT = 10
    client_credentials_manager = SpotifyClientCredentials(
        client_secret="6d5414ddba994e6191bdf59e48fab5ea",
        client_id="140259c128a34245b6e8be78e47aadf2",
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=TIMEOUT)
    return sp


@login_required
def home(request):
    sp = getsphandle()
    sp.trace = False

    sngs = []

    form = ArtistForm()

    if request.method == "POST":

        form = ArtistForm(request.POST)
        if form.is_valid():
            artname = form.cleaned_data.get("artist")
            print(artname)

            results = sp.search(q=artname, limit=20)
            for t in results["tracks"]["items"]:
                tmp = dict()
                tmp["id"] = t["id"]
                tmp["name"] = t["name"]
                tmp["art"] = t["album"]["images"][1]["url"]
                tmp["link"] = t["external_urls"]["spotify"]
                tmp["album"] = t["album"]
                tmp["duration"] = (
                    str(math.floor(t["duration_ms"] / 60000))
                    + " mins "
                    + str(
                        math.floor(
                            (
                                t["duration_ms"] / 60000
                                - math.floor(t["duration_ms"] / 60000)
                            )
                            * 60
                        )
                    )
                    + " secs "
                )
                sngs.append(tmp)

        context = {"tracks": sngs}
        return render(request, "recommendpg/home.html", context)

    else:
        form = ArtistForm()

    return render(request, "recommendpg/home.html", {"form": form})



@login_required
def recommend(request, tid):
    sp = getsphandle()
    context = {"tracks": recommendations(sp, tid)}
    return render(request, "recommendpg/recopage.html", context)


# @login_required
# def recommend(request, tid):
#     sp = getsphandle()
#     context = recommendations(sp,tid)
#     #features = pd.DataFrame(sp.audio_features(tid))
  
#     return render(request,'recommendpg/recopage.html',context)
