from django.db import models
from django.contrib.auth.models import User

class Notes(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.title

class SharedNote(models.Model):
    note = models.ForeignKey(Notes, on_delete=models.CASCADE, related_name='shared_with')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_notes')
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('note', 'shared_with')