from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Section(models.Model):
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    section_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.section_name}"

class Paragraph(models.Model):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.CharField(max_length=5000)

    def __str__(self):
        return f"{self.content}"
