from urllib import request
import random
import markdown2
from . import util
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries":util.list_entries()
    })

def entry(request,title):
            entry_content = util.get_entry(title)
            if entry_content == None:
                return render(request,'encyclopedia/error.html',{
                    'error': 'The requested page was not found',
                })
            else:
                mark_content = markdown2.markdown(entry_content)
                return render(request,'encyclopedia/entry.html',{
                    'entry_title': title,
                    'entry_content': mark_content,
            })
            

def search(request):
        if request.method == 'POST':
            # Get the words searched by user
            q = request.POST['q']
            # Get the list of all entry names
            entries = util.list_entries()
            # Change the entry names to upper case
            entries_upper = []
            for entry in entries:
              entry = entry.upper()
              entries_upper.append(entry)

            results = []
            # Check if the searched entry name is already in entry
            if q.upper() in entries_upper:
               return HttpResponseRedirect(reverse('encyclopedia:entry',args=(q,)))
            else:
                # Filter the entry names which contains search-words
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
        return HttpResponseRedirect(reverse('encyclopedia:entry',args=(title,)))

def new(request):
    if request.method == 'GET':
        return render(request,'encyclopedia/new.html')
    else:
        title =request.POST['title']
        content = request.POST['content']
        exist = util.get_entry(title)
        if exist is None:
           util.save_entry(title,content)
           return HttpResponseRedirect(reverse('encyclopedia:entry',args=(title,)))
        else:
            return render(request,'encyclopedia/error.html',{
                'message': 'Enry page already exists.',
            })
   
   

def random_page(request):
        entries = util.list_entries()
        title = random.choice(entries)
        return HttpResponseRedirect(reverse('encyclopedia:entry',args=[title]))


        
      