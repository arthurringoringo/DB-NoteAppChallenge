from django.test import TestCase
from .models import Note
from django.urls import reverse
from django.utils import timezone
from .forms import *


# Create your tests here.

                                        #CREATE TEST OF NOTES
    
class NoteCreateTest(TestCase):
            # FORM TEST AND HTML TEST
    def test_HTML(self):
        '''
        testing Which HTML template is used and the content inside
        '''
        response = self.client.get(reverse('notes:notecreate'))
        self.assertTemplateUsed(response,'notes/noteCreate.html')
        self.assertContains(response,'<label for="id_note_title">Note title:</label>')
        self.assertContains(response,'<input type="text" name="note_title" class="form-control" required id="id_note_title">')
        self.assertContains(response,'<label for="id_context">Context:</label>')
        self.assertContains(response,'<textarea name="context" cols="40" rows="4" class="form-control" required id="id_context">')
        
                #VALID TEST
    def test_create_form_valid(self):
        '''
        returns true if note is valid
        '''
        form = CreateForm(data={'note_title':'Titleone','context':'This is a test'})
        self.assertTrue(form.is_valid())
                #INVALID TEST
    def test_create_form_invalid_incomplete(self):
        '''
        returns false if note only contains title
        '''
        form = CreateForm(data={'note_title':'Titleone','context':''})
        self.assertFalse(form.is_valid())

    def test_create_form_invalid_empty(self):
        '''
        returns false if note does not contain any data
        '''
        form = CreateForm(data={'note_title':'','context':''})
        self.assertFalse(form.is_valid())

    def test_create_form_invalid_incomplete_title(self):
        '''
        returns false if note only contains Context
        '''
        form = CreateForm(data={'note_title':'','context':'This is a test'})
        self.assertFalse(form.is_valid())


                                        #READ TEST OF NOTES


class NoteHTMLResponseTest(TestCase):
    def test_page_status(self):
        '''
        Test the status code of the page, if this pass then page is working fine
        '''
        url = reverse('notes:notelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
            #VALID READ TEST
class NoteReadTest(TestCase):
    
    def setUp(self):
        '''
        Create Data needed for the test
        '''
        note = Note.objects.create(note_title  = "TestNote",creation_date=timezone.now(),modify_date=timezone.now(),context="This is a test 123")
    
    def test_read_notes(self):
        '''
        Returns the object NoteList with the created note as object within it
        '''
        response = self.client.get(reverse('notes:notelist'))
        self.assertEqual(response.status_code,200)
        self.assertQuerysetEqual(response.context['NoteList'],['<Note: TestNote>'])

    def test_HTML(self):
        '''
        testing Which HTML template is used and the content inside
        '''
        response = self.client.get(reverse('notes:notelist'))
        self.assertTemplateUsed(response,'notes/notes.html')
        self.assertContains(response,'<a href="/notes/1/view/" class="list-group-item list-group-item-action"> TestNote </a>')

    
            # INVALID READ TEST
class invalidNoteReadTest(TestCase):
    
    def test_read_notes_invalid(self):
        '''
        Returns NoteList with no objects if notes in NoteList does not exist
        '''
        response = self.client.get(reverse('notes:notelist'))
        self.assertQuerysetEqual(response.context['NoteList'],[])



                                    #UPDATE NOTES TEST
class NoteUpdateTest(TestCase):
    def setUp(self):
        '''
        Create Data needed for the test
        '''
        Note.objects.create(note_title  = "TestNote",creation_date=timezone.now(),modify_date=timezone.now(),context="This is a test 123")
       

    def test_page_status(self):
        '''
        Test the status code of the page, if this pass then page is working fine
        '''
        note = Note.objects.get(pk=1)
        url = reverse('notes:noteview',args=(note.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_HTML(self):
        '''
        testing Which HTML template is used and the content inside
        '''
        note = Note.objects.get(pk=1)
        exp = "<h2> "+note.note_title+" </h2>"
        exp2 = '<textarea class="form-control" name="NoteContext" id="NoteContext" rows="5">'+note.context
        response = self.client.get(reverse('notes:noteview' ,args=(note.id,)))
        self.assertTemplateUsed(response,'notes/noteView.html')
        self.assertContains(response,exp)
        self.assertContains(response,exp2)

    def test_update_function(self):
        '''
        testing the update function
        '''
        note = Note.objects.get(pk=1)
        response = self.client.post(reverse('notes:noteupdate',args=(note.id,)),
        {'NoteContext':'this is a test update 123'})
        self.assertEqual(response.status_code,302)
        note.refresh_from_db()
        self.assertEqual(note.context,'this is a test update 123')


                    #DELETE NOTES TEST

class NoteDeleteTest(TestCase):
    def setUp(self):
        '''
        create the data needed for the test
        '''
        Note.objects.create(note_title  = "TestNote",creation_date=timezone.now(),modify_date=timezone.now(),context="This is a test 123")

    def test_delete_function(self):
        '''
        testing the delete function
        '''
        note = Note.objects.get(pk=1)
        response = self.client.post(reverse('notes:notedelete',args=(note.id,)))
        self.assertEqual(response.status_code,302)
        self.assertFalse(Note.objects.filter(pk=1).exists())
    
    def test_delete_function(self):
        '''
        testing the redirects of delete function to a correct file
        '''
        note = Note.objects.get(pk=1)
        response = self.client.post(reverse('notes:notedelete',args=(note.id,)))
        self.assertEqual(response.status_code,302)
        self.assertFalse(Note.objects.filter(pk=1).exists())
        
