from django.shortcuts import render
import numpy as np


# Create your views here.
def index(request):
    return render(request, "index.html")


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
