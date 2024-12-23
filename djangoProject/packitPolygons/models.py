from django.db import models


class Game(models.Model):
    size = models.IntegerField()
    board = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    turns = models.IntegerField()
    # mode = models.CharField(max_length=10)
    triangular_mode = models.BooleanField()
    ai_mode = models.BooleanField()
    ai_starts = models.BooleanField(null=True)
