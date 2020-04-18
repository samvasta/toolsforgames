from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from .serializers import TableSerializer, TableDetailsSerializer, TableRowSerializer, TableResultSerializer
from .models import Table, TableRow, TableResult

import random

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

class RollViewSet(viewsets.ViewSet):

    def roll(self, request, table_id=None):
        count = int(request.query_params.get('n') or 1)
        rows = TableRow.objects.all().filter(table_id__exact=table_id).order_by('index_start')

        weights = [row.index_end - row.index_start + 1 for row in rows]

        choices = random.choices(population=rows, weights=weights, k=count)

        unique_rows = set(choices)

        get_results = lambda x : list(map(lambda x: x.result, TableResult.objects.all().filter(table_row_id__exact=x.id).order_by('order')))

        row_id_to_results = dict((row.id, get_results(row)) for row in unique_rows)

        results = [{'n': i+1, 'row_id': x.id, 'results': row_id_to_results.get(x.id)} for i, x in enumerate(choices)]

        data = { 'table_id' : table_id, 'count': count, 'rolls': results }

        return Response(data)