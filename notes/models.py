from django.db import models
from django.utils import timezone
import datetime

class Note(models.Model):
    note_title = models.CharField(max_length=55, unique=True)
    creation_date = models.DateTimeField('Created on',default=timezone.now)
    modify_date = models.DateTimeField('Modified on',default=timezone.now)
    context = models.TextField()
    def __str__(self):
        return self.note_title
    