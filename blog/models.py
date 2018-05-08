from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()


class Entry(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    entry_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, default=0, on_delete=models.CASCADE)
