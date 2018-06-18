# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .serializers import *
from .models import *
from .zomato_scrape import *
import os

CWD=os.getcwd()
cdir=CWD

#Trigger the task
@shared_task
def scrape_zomato():
    print "Task Init"
    zomato_scrape()
