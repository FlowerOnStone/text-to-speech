from django.contrib import admin
from .models import Section, Paragraph

# Register your models here.
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["username", "section_name"]

@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ["section", "content"]
