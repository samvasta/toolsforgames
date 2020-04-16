from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from .serializers import TableSerializer, TableDetailsSerializer, TableRowSerializer, TableResultSerializer
from .models import Table, TableRow, TableResult

class TableViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = Table.objects.all().order_by('table_name')
        serializer_context = {
            'request': request,
        }
        serializer = TableSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Table.objects.all()
        table = get_object_or_404(queryset, pk=pk)
        serializer = TableDetailsSerializer(table)
        return Response(serializer.data)

    
class TableRowViewSet(viewsets.ModelViewSet):
    queryset = TableRow.objects.all().order_by('table_id', 'index_start')
    serializer_class = TableRowSerializer

class TableResultViewSet(viewsets.ModelViewSet):
    queryset = TableResult.objects.all().order_by('table_row_id', 'order')
    serializer_class = TableResultSerializer