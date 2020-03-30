from django.urls.resolvers import URLPattern
from django.urls import path
from . import views

app_name='notes'
urlpatterns = [
    path('',views.NoteList.as_view(), name="notelist"),
    path('<str:pk>/view/',views.NoteView.as_view(), name="noteview"),
    path('create/', views.NoteCreate,name="notecreate"),
    path('<int:note_id>/update/', views.NoteUpdate,name="noteupdate"),
    path('<int:note_id>/delete/', views.NoteDelete, name="notedelete")
]
