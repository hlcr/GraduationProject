from json import JSONEncoder

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from OpinionMonitor.models import Passage
from django.shortcuts import render
from .tool import *
from .models import kwl
from .models import fpl
import json
from collections import OrderedDict

# Create your views here.
class IndexView(generic.DetailView):
    template_name = 'OM/index.html'


def index(request):
    return render(request, 'OM/index.html')

def sim_txt(request):
    return render(request, 'OM/sim_txt.html')

def hot(request):
    return render(request,'OM/echart.html')

def search(request):
    page = 0
    if request.method == 'GET':
        if "keyword" in request.GET:
            keyword = request.GET["keyword"]
            print(keyword)
            if "page" in request.GET:
                page = int(request.GET["page"])
            else:
                page = 1
            context = get_search_result(keyword, page)
    return render(request, 'OM/list.html', context)


def sim_txt_result(request):
    r_dict = dict()
    if request.method == 'POST':
        if "s_text" in request.POST:
            r_dict = get_similar_text(request.POST['s_text'])
    return HttpResponse(json.dumps(r_dict, ensure_ascii=False))


def get_keyword_list(request):
    num = 10
    if 'num' in request.GET:
        num = int(request.GET['num'])
    key_word_list = kwl.objects.order_by("-num")[0:num]
    r_list = []
    for keyword in key_word_list:
        w_tuple = keyword.to_tuple()
        r_list.append(w_tuple)
    r_dict = OrderedDict(r_list)
    return HttpResponse(json.dumps(r_dict, ensure_ascii=False))


def get_focus_passge_list(request):
    passage_list = fpl.objects.order_by("-c_read")[0:10]
    r_list = []
    for passage in passage_list:
        p_tuple = passage.to_tuple()
        r_list.append(p_tuple)
    r_dict = OrderedDict(r_list)
    return HttpResponse(json.dumps(r_dict, ensure_ascii=False))

