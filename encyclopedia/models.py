from django.db import models

# Create your models here.

class Entry(models.Model):
    entry_title = models.CharField(max_length=200,primary_key=True)
    entry_content = models.TextField()
    
    def __str__(self):
        return self.entry_title