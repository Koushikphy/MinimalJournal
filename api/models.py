from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# class Tag(models.Model):
#     name = models.CharField(max_length=255) 



# tag is not requires at this momoneet we will just search throughthe desc field initiall
class Entries(models.Model):
    desc = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # tags this time is just some keyword seperated by comma, that is searchable
    tags = models.TextField(blank=True)
    # tags = models.ManyToManyField(Tag, related_name='tag')
