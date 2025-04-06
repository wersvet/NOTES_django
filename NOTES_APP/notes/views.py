from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Notes
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import NotesForm

from django.contrib.auth.mixins import LoginRequiredMixin


from django.shortcuts import render, redirect
from .models import Notes, SharedNote
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View  # Добавляем этот импорт
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notes, SharedNote
from .forms import NotesForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = 'notes'
    login_url = '/login/'
    template_name = 'notes/note_list.html'

    def get_queryset(self):
        # Собственные заметки
        own_notes = self.request.user.notes.all()
        # Заметки, которыми поделились
        shared_notes = Notes.objects.filter(shared_with__shared_with=self.request.user)
        return (own_notes | shared_notes).distinct()

class NotesDetailView(LoginRequiredMixin, DetailView):
    model = Notes
    context_object_name = 'note'
    login_url = '/login/'

    def get_queryset(self):
        # Доступны свои заметки и те, которыми поделились
        own_notes = self.request.user.notes.all()
        shared_notes = Notes.objects.filter(shared_with__shared_with=self.request.user)
        return (own_notes | shared_notes).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user  # Проверяем, владелец ли
        return context
    

class NotesCreateView(LoginRequiredMixin, CreateView):
    model = Notes
    success_url = '/smart/notes/'
    form_class = NotesForm
    login_url = '/login/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class NotesUpdateView(LoginRequiredMixin, UpdateView):
    model = Notes
    success_url = '/smart/notes/'
    form_class = NotesForm
    login_url = '/login/'

    def get_queryset(self):
        return self.request.user.notes.all()

class NotesDeleteView(LoginRequiredMixin, DeleteView):
    model = Notes
    success_url = '/smart/notes/'
    context_object_name = 'note'
    template_name = 'notes/notes_delete.html'
    login_url = '/login/'

    def get_queryset(self):
        return self.request.user.notes.all()
    

class ShareNoteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        note = Notes.objects.get(pk=pk)
        if note.user != request.user:
            return HttpResponse("Вы не можете делиться этой заметкой.", status=403)
        
        username = request.POST.get('username')
        try:
            user_to_share = User.objects.get(username=username)
            if user_to_share == request.user:
                return HttpResponse("Нельзя поделиться с самим собой.")
            SharedNote.objects.get_or_create(note=note, shared_with=user_to_share)
            return redirect('notes.detail', pk=note.pk)
        except User.DoesNotExist:
            return HttpResponse("Пользователь не найден.")