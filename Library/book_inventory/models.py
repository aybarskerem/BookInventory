from django.db import models

# Create your models here.

class BookInventory(models.Model):
    author = models.CharField(max_length=50,  default='Anonymous')
    title  = models.CharField(max_length=250, default="No Title")
    number_of_pages = models.IntegerField()
    published_date  = models.DateField(default='1970-01-31')

    def __str__(self):
        return f'{self.title} ({self.author})'