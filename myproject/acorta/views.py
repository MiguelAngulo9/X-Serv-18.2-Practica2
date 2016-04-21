from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import url_a_acortar
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

# Create your views here.

@csrf_exempt
def procesar_URLs(request):
    urls = ""
    if request.method == "GET":
        lista_urls = url_a_acortar.objects.all()
        urls = "<ol>"
        for url in lista_urls:
            urls += '<pre>' + str(url.id) + '. ' + url.URL
        urls += "<ol>"
        template = get_template('formulario.html')
        Context = ({'contenido': urls})
        Formulario = template.render(Context)
        return HttpResponse(Formulario)
    elif request.method == "POST":
        url = request.POST.get("url")
        if url == "":
            Respuesta = "<b>Entrada no valida. La URL esta vacia</b>"
            return HttpResponse(Respuesta)
        elif not url.startswith("https://") and not url.startswith("http://"):
            url = "http://" + url
        try:
            url_nueva = url_a_acortar.objects.get(URL=url)
        except url_a_acortar.DoesNotExist:
            url_nueva = url_a_acortar(URL=url)
            url_nueva.save()
        Respuesta = "<p><b>Id de la URL que se ha acortado: " + str(url_nueva.id) + "</b></p>"
        Respuesta += "<a href=" + str(url_nueva.id) + "> 1. Haz click aqui si desea ir a la pagina que ha solicitado</a></br></br>"
        Respuesta += "<a href=''> 2. Haz click aqui para volver atras</a>"
        template = get_template('plantilla.html')
        Context = ({'contenido':Respuesta})
        Plantilla = template.render(Context)
        return HttpResponse(Plantilla)


def redireccion_a_real_URL(request, identificador):
    try:
        url = url_a_acortar.objects.get(id=identificador)
    except url_a_acortar.DoesNotExist:
        Respuesta = "<b>La URL con Id = " + str(identificador) + " no se encuentra en la lista --> RECURSO NO DISPONIBLE</b>"
        return HttpResponse(Respuesta)
    Pagina_Real = url.URL
    return HttpResponseRedirect(Pagina_Real)
