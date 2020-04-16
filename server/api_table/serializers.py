from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Table, TableRow, TableResult

class TableResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TableResult
        fields = ['result', 'order']

class TableRowSerializer(serializers.ModelSerializer):
    table_id = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all())
    results = serializers.SerializerMethodField()

    class Meta:
        model = TableRow
        fields = ['table_id', 'index_start', 'index_end', 'results']

    def get_results(self, instance):
        results = instance.results.all().order_by('order')
        return TableResultSerializer(results, many=True).data

class TableSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    url = serializers.HyperlinkedIdentityField(view_name='table-detail')

    class Meta:
        model = Table
        fields = ['url', 'table_name', 'created_by', 'description', 'date_created']

        
class TableDetailsSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    rows = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ['table_name', 'created_by', 'description', 'date_created', 'rows']

    def get_rows(self, instance):
        rows = instance.rows.all().order_by('index_start')
        return TableRowSerializer(rows, many=True).data