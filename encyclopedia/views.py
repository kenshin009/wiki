from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


from . import util
from django.urls import reverse
import markdown2

import random
from random import choice



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries":util.list_entries()
    })

def entry(request,title):
            entry_content = util.get_entry(title)
            if entry_content == None:
                return render(request,'encyclopedia/error.html',{
                    'error': 'This entry does not exist',
                })
            else:
                mark_content = markdown2.markdown(entry_content)
                return render(request,'encyclopedia/entry.html',{
                    'entry_title': title,
                    'entry_content': mark_content,
            })
            

def search(request):
        if request.method == 'POST':
            q = request.POST['q']
            entries = util.list_entries()
            results = []
            if q in entries:
               return HttpResponseRedirect(reverse('encyclopedia:entry',args=(q,)))
            else:
                for entry in entries:
                    if q.upper() in entry.upper():
                        results.append(entry)
                return render(request,'encyclopedia/results.html',{     
                    'results': results,
                })
                         
                      
def edit(request,title):
        if request.method == 'GET':
            return render(request,'encyclopedia/edit.html',{
                'title': title,
                'content': util.get_entry(title),
        })
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST['content']
            util.save_entry(title,content)
        return HttpResponseRedirect(reverse('encyclopedia:entry',args=[title]))

def new(request):
    if request.method == 'GET':
        return render(request,'encyclopedia/new.html')
    else:
        title =request.POST['title']
        content = request.POST['content']
        exist = util.get_entry(title)
        if exist is None:
           util.save_entry(title,content)
           return HttpResponseRedirect(reverse('encyclopedia:entry',args=[title]))
        else:
            return render(request,'encyclopedia/error.html',{
                'message': 'Enry page already exists.',
            })
   
   

def random_page(request):
        entries = util.list_entries()
        title = random.choice(entries)
        return HttpResponseRedirect(reverse('encyclopedia:entry',args=[title]))


        
      