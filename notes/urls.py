from django.urls.resolvers import URLPattern
from django.urls import path
from . import views

app_name='notes'
urlpatterns = [
    path('',views.NoteList.as_view(), name="notelist"),
    path('<int:pk>/view/',views.NoteView.as_view(), name="noteview"),
    path('create/', views.NoteCreate,name="notecreate")
]
