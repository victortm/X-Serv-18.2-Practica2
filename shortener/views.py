from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import Url
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def shortener(request):
    if request.method == "GET":
        urlDb = Url.objects.all()
        urlDic = ""
        for url in urlDb:
            urlDic +=  "URL " + str(url.url) + " Shortened URL " + str(url.id) + "<br/>"

        resp = "<body><html> <form id= shortUrl method= post> \
                <fieldset><legend>URL shortener</legend><label> Url</label> \
                <input id= campo1 name= Url type= text /></label> \
                <input id= campo2 name= pressbutton type= submit value= Shorten URL/> \
                </fieldset> </form> <p> URL Dictionary </p>" \
                + urlDic + "</body></html>"
       
    elif request.method == "POST":
        url = request.body.split("=")
        url = url[1].split("&")
        url = url[0]
        try:
            url = Url.objects.get(url = url)
        except Url.DoesNotExist:
            new = Url(url = url)
            new.save()
        urlId = str(Url.objects.get(url = url).id) 
        resp = "<html><body>URL " + url + " Shortened URL \
                <a href= http://" + url + ">" + urlId + "</a> \
                </body></html>"

    return HttpResponse(resp)

def redir(request, resource):
    if request.method == "GET":
        try:
            short = Url.objects.get(id = resource).url
            resp = "<html><body> \
                   <meta http-equiv= refresh content= 1;url=http://" \
                   + short + "> </body></html>"
            return HttpResponse(resp)
        except Url.DoesNotExist:
            return HttpResponseNotFound("Shortened URL " + resource + " is not available")
