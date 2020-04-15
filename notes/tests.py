from django.test import TestCase
from .models import Note
from django.urls import reverse
from django.utils import timezone


# Create your tests here.

def create_note(title,context):
    """
    Function to create A Note
    """
    timenow = timezone.now()
    return Note.objects.create(note_title=title,creation_date=timenow,modify_date=timenow,context=context)

class NoteCreateTest(TestCase):
