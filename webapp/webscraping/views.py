from django.conf.urls import url
from django.shortcuts import render
from django.http import HttpResponse
import requests
from requests.sessions import Request

# Create your views here.
def get_html_content(urlsite):
    import requests
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE

    if urlsite == 'g1':
        html_content=session.get('https://g1.globo.com/').text
    elif urlsite == 'r7':
        html_content = session.get('https://www.r7.com/').text
    elif urlsite == 'uol':
        html_content = session.get('https://www.uol.com.br/').text
        
    return html_content

def home(request):
    noticiasG1_title=None
    noticiasG1_txttag1Title = []

    noticiasR7_title = None
    noticiasR7_txttag1title = []

    noticiasUOL_title = None
    noticiasUOL_txttag1title = []

    contreg = 0
    from bs4 import BeautifulSoup
    urlsite= ''
    if 'g1' in request.GET:
        urlsite = 'g1'
        html_content = get_html_content(urlsite)
        #print(html_content)

        source = BeautifulSoup(html_content, 'html.parser')
        noticiasG1_title= source.findAll('a', attrs={'class': 'feed-post-link gui-color-primary gui-color-hover'})
        #noticiasG1_subtitle= source.findAll('div', attrs={'class': 'feed-post-body-resumo'})

        for i in noticiasG1_title:
            noticiasG1_txttag1Title.append(i.text)
        
        contreg=int(len(noticiasG1_txttag1Title))

        '''for i in noticiasG1_subtitle:
            noticiasG1_txttag1subTitle.append(i.text)'''

        #print(noticiasG1_txttag1subTitle)

        

    elif 'r7' in request.GET:
        urlsite = 'r7'
        html_content = get_html_content(urlsite)
        #print(html_content)
        source = BeautifulSoup(html_content, 'html.parser')
        noticiasR7_title = source.findAll('h3', attrs={'class': 'r7-flex-title-h5'})
        
        for i in noticiasR7_title:
            noticiasR7_txttag1title.append(i.text)

        contreg=int(len(noticiasR7_txttag1title))
            
        

    elif 'uol' in request.GET:
        urlsite = 'uol'
        html_content = get_html_content(urlsite)
        source = BeautifulSoup(html_content, 'html.parser')
        noticiasUOL_title = source.findAll('h2', attrs={'class': 'titulo color2'})

        for i in noticiasUOL_title:
            noticiasUOL_txttag1title.append(i.text)

        contreg=int(len(noticiasUOL_txttag1title))

    return render(request, 'webscraping/scraping.html', {'noticiasG1_txttag1Title': noticiasG1_txttag1Title, 
                                                      'noticiasR7_txttag1title': noticiasR7_txttag1title, 
                                                      'noticiasUOL_txttag1title': noticiasUOL_txttag1title,
                                                      'contreg': contreg})
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

# Create your models here.

class USUARIO(models.Model):
    email = models.EmailField(max_length=128, blank=False)
    nome = models.CharField(max_length=64, blank=False)
    senha = models.CharField(max_length=64, blank=False)
    data_scrap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class TWEETS(models.Model):
    tweet_usuario = models.CharField(max_length=32, blank=False)
    tweet_username = models.CharField(max_length=32, blank=False)
    tweet_hora = models.CharField(max_length=20, blank=False)
    tweet_texto = models.CharField(max_length=256, blank=True)
    tweet_answer = models.CharField(max_length=256, blank=True)
    tweet_qtdretweets = models.CharField(max_length=10, blank=True)
    tweet_qtdcomments = models.CharField(max_length=10, blank=True)
    tweet_qtdlikes = models.CharField(max_length=10, blank=True)

    usuario = models.ForeignKey(USUARIO, on_delete=models.CASCADE)

    def __str__(self):
        return self.tweets



from django.contrib import admin
from .models import TWEETS, USUARIO

# Register your models here.

admin.site.register(USUARIO)

admin.site.register(TWEETS)
