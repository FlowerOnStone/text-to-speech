from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from gtts import gTTS
import os
from .models import Section, Paragraph
import random
import string
from .forms import CreateSectionForm, CreateSentenceForm
from django.urls import reverse


# Create your views here.
def get_random_filename():
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(30))
    return result


def get_media_url(request):
    if "text" in request.POST:
        paragraph = request.POST["text"]
        language = 'vi'
        myobj = gTTS(text=paragraph, lang=language, slow=False)
        filename = get_random_filename() + ".mp3"
        myobj.save(os.path.join('media', filename))
        return '/media/' + filename
    return ""


def index(request):
    template = loader.get_template("index.html")
    paragraph = ""
    if "test" in request.POST:
        paragraph = request["text"]
    sections = []
    if request.user.username:
        sections = Section.objects.filter(username=request.user)
    context = {
        "paragraph": paragraph,
        "media_url": get_media_url(request),
        "id": 0,
        "sections": sections,
    }
    return HttpResponse(template.render(context, request))


def common_sentence(request):
    template = loader.get_template("common_sentence.html")
    sentences = Paragraph.objects.filter(section=Section.objects.get(section_name="common_sentence")).values()
    sections = []
    if request.user.username:
        sections = Section.objects.filter(username=request.user)
    context = {
        "media_url": get_media_url(request),
        "sentences": sentences,
        "id": 1,
        "sections": sections,
    }
    return HttpResponse(template.render(context, request))


def create_section(request):
    if not request.user.username:
        return HttpResponseRedirect('/')
    form = CreateSectionForm()
    if request.method == 'POST':
        form = CreateSectionForm(request.POST)
        if form.is_valid():
            section_id = form.save(request.user)
            return HttpResponseRedirect(reverse('view_section', args=[section_id]))
    template = loader.get_template('create_section.html')
    sections = []
    if request.user.username:
        sections = Section.objects.filter(username=request.user)
    context = {
        "sections": sections,
        "form": form,
    }
    return HttpResponse(template.render(context, request))


def view_section(request, id):
    if request.user.id != Section.objects.get(id=id).username.id:
        return HttpResponseRedirect('/')
    template = loader.get_template("section.html")
    sentences = Paragraph.objects.filter(section=Section.objects.get(id=id)).values()
    sections = []
    if request.user.username:
        sections = Section.objects.filter(username=request.user)
    context = {
        "media_url": get_media_url(request),
        "sentences": sentences,
        "id": id,
        "sections": sections,
    }
    return HttpResponse(template.render(context, request))


def create_sentence(request, id):
    if request.user.id != Section.objects.get(id=id).username.id:
        return HttpResponseRedirect('/')
    template = loader.get_template("create_sentence.html")
    form = CreateSentenceForm()
    if request.method == 'POST':
        form = CreateSentenceForm(request.POST)
        if form.is_valid():
            form.save(Section.objects.get(id=id))
            return HttpResponseRedirect(reverse('view_section', args=[id]))
    sections = []
    if request.user.username:
        sections = Section.objects.filter(username=request.user)
    current_section_name = Section.objects.get(id=id).section_name
    context = {
        "media_url": get_media_url(request),
        "id": id,
        "sections": sections,
        "current_section_name": current_section_name,
        "form": form,
    }
    return HttpResponse(template.render(context, request))


def edit_sentence(request, id):
    template = loader.get_template("edit_sentence.html")
    sections = []
    if request.user.username:
        sections = Section.objects.filter(username=request.user)
    paragraph = Paragraph.objects.get(id=id)
    if request.user.id != paragraph.section.username.id:
        return HttpResponseRedirect('/')
    context = {
        "media_url": get_media_url(request),
        "id": id,
        "sections": sections,
        "paragraph": paragraph,
    }
    return HttpResponse(template.render(context, request))


def update_sentence(request):
    paragraph = Paragraph.objects.get(id=request.POST['id'])
    paragraph.content = request.POST['content']
    paragraph.save()
    return HttpResponseRedirect(reverse('view_section', args=[paragraph.section.id]))


def delete_sentence(request, id):
    paragraph = Paragraph.objects.get(id=id)
    paragraph.delete()
    return HttpResponseRedirect('/')


def delete_section(request, id):
    section = Section.objects.get(id=id)
    if request.user.id != section.username.id:
        return HttpResponseRedirect('/')
    section.delete()
    return HttpResponseRedirect('/')


def edit_section(request, id):
    template = loader.get_template("edit_section.html")
    sections = []
    if request.user.username:
        sections = Section.objects.filter(username=request.user)
    section = Section.objects.get(id=id)
    if request.user.id != section.username.id:
        return HttpResponseRedirect('/')
    context = {
        "media_url": get_media_url(request),
        "id": id,
        "sections": sections,
        "section": section,
    }
    return HttpResponse(template.render(context, request))


def update_sectiom(request):
    section = Section.objects.get(id=request.POST['id'])
    section.section_name = request.POST["section_name"]
    section.save()
    return HttpResponseRedirect(reverse('view_section', args=[section.id]))


def error(request, exception):
    return HttpResponseRedirect('/')