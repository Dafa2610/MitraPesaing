from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(max_length=3)
    email = models.TextField()

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email