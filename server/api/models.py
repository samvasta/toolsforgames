from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Table(models.Model):
    table_name      = models.CharField(max_length=50)                                # Plain text
    description     = models.TextField()                                            # Markdown text
    date_created    = models.DateTimeField(default=timezone.now)
    created_by      = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.table_name
    


class TableRow(models.Model):
    table_id        = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='rows')
    index_start     = models.PositiveIntegerField()
    index_end       = models.PositiveIntegerField()

    def __str__(self):
        if self.index_start == self.index_end:
            return f'{self.index_start}'
        else:
            return f'[{self.index_start} - {self.index_end}]'
    
    
class TableResult(models.Model):
    table_row_id    = models.ForeignKey(TableRow, on_delete=models.CASCADE, related_name='results')
    result          = models.TextField()
    order           = models.PositiveIntegerField()

    def __str__(self):
        return self.result