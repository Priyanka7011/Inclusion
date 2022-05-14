from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
import json
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth import logout
from .Recommendersys import *
from .RecommenderUser import *
from .models import *
import pandas as pd
import numpy as np
import requests

# Create your views here.
def index(request):
    return render(request, "index.html")


def logout_view(request):
    logout(request)

    return redirect("index")


from django.shortcuts import render
import numpy as np


# Create your views here.
def index(request):
    return render(request, "index.html")


def repo_rec(request):

    if request.method == "POST":
        print("hello")
        data = request.POST.get("data")
        desc = request.POST.get("desc")

        for word in data:
            desc += word

        print(desc)

        df = pd.DataFrame((list(GithubRepos.objects.all().values())))
        print(df.head())
        dictionary, tfidf, index, lsi = fit_repos(df["content"])
        # print(cosine_sim)
        repo_list = recommendations(dictionary, tfidf, index, lsi, desc)
        # print(repo_list[0][9])
        for repo in repo_list:
            print("hello world",repo[9][9:])
            repo[9]=repo[9][9:]

        context = {"repo_list": repo_list}

        return render(request, "repo_rec.html", context)

    # list_repo=model.recommendations("sample code for several design patterns in PHP 8 ['code-examples', 'design-pattern', 'design-patterns', 'designpatternsphp', 'hacktoberfest', 'modern-php', 'oop', 'php', 'php8', 'phpunit'] dict_keys(['PHP', 'Python', 'Makefile', 'Dockerfile'])")
    # print(list_repo)

    return render(request, "repo_rec.html")


def form_contributors_res(request):

    lang_token, token_list = lang_topic_list()
    context = {
        "token_list": token_list,
        "lang_token": lang_token,
    }

    return render(request, "form_contributors.html", context)


def lang_topic_list():
    lang_list = list(GithubRepos.objects.all().values("languages"))
    topic_list = list(GithubRepos.objects.all().values("topics"))
    # print(lang_list)
    size = len(topic_list)
    print(size)
    token_list = []
    lang_token = []
    for i in range(0, size):
        temp = topic_list[i]["topics"].split("'")
        lang_temp = lang_list[i]["languages"].split("'")
        stop_words = ["[", "]", ",", ", ", "[]", "([", "([])", "])", ", "]
        for k in lang_temp:
            if k not in stop_words:
                lang_token.append(" " + k + " ")
        for j in temp:
            if j not in stop_words:
                token_list.append("  " + j + " ")

    # [0]['topics'].split("'")[3]
    token_list = np.array(token_list)
    token_list = np.unique(token_list)
    lang_token = np.array(lang_token)
    lang_token = np.unique(lang_token)

    return lang_token, token_list


def form_res(request):

    lang_token, token_list = lang_topic_list()
    print(lang_token)
    context = {
        "token_list": token_list,
        "lang_token": lang_token,
    }
    return render(request, "form.html", context)


def user_rec(request):
    if request.method == "POST":
        print("hello")
        data = request.POST.get("data")
        desc = request.POST.get("desc")

        for word in data:
            desc += word

        print(desc)

        df = pd.DataFrame((list(GithubUsers.objects.all().values())))
        print(df.head())
        dictionary, tfidf, index, lsi = fit(df["all_repos"])
        # print(cosine_sim)
        user_list, user_expert = user_recs(dictionary, tfidf, index, lsi, desc)
        # print(user_list[0])

        print(user_expert[0])

        context = {"user_list": user_list}

    return render(request, "user_rec.html", context)


def org_recs(request):
    if request.user.is_authenticated:
        owner = request.user.username
        print(owner)
        repos = requests.get(
            "https://api.github.com/search/repositories?q=user:" + owner + "+sort:stars"
        ).json()
        print(repos)
        repo_det = " "
        for repo in repos["items"]:
            repo_name = str(repo["name"])
            language = str(repo["language"])
            topic = str(repo["topics"])
            # repo_info = requests.get('https://api.github.com/repos/'+owner+'/'+repo_name)

            desc = str(repo["description"])
            repo_det += repo_name + " " + language + " " + desc + " " + topic + " "

        # print(repo_det)

        df = pd.DataFrame((list(GithubUsers.objects.all().values())))
        print(df.head())
        dictionary, tfidf, index, lsi = fit(df["all_repos"])
        # print(cosine_sim)
        user_orgs = orgs_recs_user(dictionary, tfidf, index, lsi, desc)
        print(user_orgs)

        org_desc = ["a"] * len(user_orgs)

        for i in range(len(user_orgs)):
            org = user_orgs[i]
            org_url = "https://github.com/" + org
            org_det = requests.get("https://api.github.com/orgs/" + org).json()
            org_desc[i] = [org, org_det["avatar_url"], org_det["public_repos"], org_url]

        print(org_desc)

        context = {"user_orgs": org_desc}

        return render(request, "org_rec.html", context)
    return render(request, "org_rec.html")
