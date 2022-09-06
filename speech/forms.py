from django import forms
import re
from django.contrib.auth.models import User
from .models import Section, Paragraph


class CreateSectionForm(forms.Form):
    name = forms.CharField(label='Tài khoản', max_length=30, widget=forms.TextInput(attrs={'class': "form-control"}))

    def clean_name(self):
        if "name" in self.cleaned_data:
            return self.cleaned_data['name']
        raise forms.ValidationError("Bạn chưa nhập tên cuộc hội thoại")

    def save(self, user):
        section = Section.objects.create(username=user, section_name=self.cleaned_data['name'])
        section.save()
        return section.id


class CreateSentenceForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", 'name': 'content', 'rows': '10'}))

    def clean_content(self):
        if "content" in self.cleaned_data:
            return self.cleaned_data['content']
        raise forms.ValidationError("Bạn chưa nhập nội dung câu nói")

    def save(self, section):
        Paragraph.objects.create(section=section, content=self.cleaned_data['content']).save()
