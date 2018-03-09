# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    view = "template_two"
    return render(request, "team/html/team.html", {'name': view})