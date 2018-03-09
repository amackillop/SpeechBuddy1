# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


# Create your views here.
def index(request):
    view = "template_two"
    return render(request, "home/html/index.html", {'name': view})