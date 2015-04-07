from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from untitledproject1.nomeste.models import Nomeste
from untitledproject1.nomeste.serializers import NomesteSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def nomeste_list(request):
    """
    List all code nomestes, or create a new epnumos.
    """
    if request.method == 'GET':
        nomestes = Nomeste.objects.all()
        serializer = NomesteSerializer(nomestes, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NomesteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def nomeste_detail(request, pk):
    """
    Retrieve, update or delete a code epnumos.
    """
    try:
        nomeste = Nomeste.objects.get(pk=pk)
    except Nomeste.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = NomesteSerializer(nomeste)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NomesteSerializer(nomeste, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        nomeste.delete()
        return HttpResponse(status=204)