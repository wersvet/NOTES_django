from django.shortcuts import render
from .models import Notes
from django.views.generic import ListView, DetailView, CreateView
from .forms import NotesForm

class NotesListView(ListView):
    model = Notes
    context_object_name = 'notes'

class NotesDetailView(DetailView):
    model = Notes
    context_object_name = 'note'

class NotesCreateView(CreateView):
    model = Notes
    fields = ['title', 'text']
    success_url = '/smart/notes/'
    form_class = NotesForm

