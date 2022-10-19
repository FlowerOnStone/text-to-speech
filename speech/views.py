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

def get_sections(request):
    sections = []
    if request.user.username:
        sections = Section.objects.filter(username=request.user).exclude(section_name="hidden_section")
    return sections


def clear_index_history(request):
    if request.user.username:
        latest_sentences = Paragraph.objects.filter(section=Section.objects.filter(username=request.user)
                                                   .get(section_name="hidden_section"))
        for latest_sentence in latest_sentences:
            latest_sentence.section = None
            latest_sentence.save()
    return HttpResponseRedirect(reverse('index'))


def index(request):
    template = loader.get_template("index.html")
    paragraph = ""
    if "text" in request.POST:
        paragraph = request.POST["text"]
    latest_sentences = []
    if request.user.username:
        if paragraph != "" and "add" in request.POST:
            Paragraph.objects.create(section=Section.objects.filter(username=request.user)
                                     .get(section_name="hidden_section"),
                                     content=paragraph).save()
        latest_sentences = Paragraph.objects.filter(section=Section.objects.filter(username=request.user)
                                                   .get(section_name="hidden_section")).order_by("id").values()
        latest_sentences = latest_sentences.reverse()
    tmp = []
    for sentence in latest_sentences:
        flag = True
        for x in tmp:
            if sentence["content"] == x["content"]:
                flag = False
                break
        if flag:
            tmp.append(sentence)
        if len(tmp) == 20:
            break
    latest_sentences = tmp
    print(tmp)
    context = {
        "paragraph": paragraph,
        "media_url": get_media_url(request),
        "id": 0,
        "sections": get_sections(request),
        "latest_sentences": latest_sentences,
    }
    return HttpResponse(template.render(context, request))


def common_sentence(request):
    template = loader.get_template("common_sentence.html")
    sentences = Paragraph.objects.filter(section=Section.objects.get(section_name="common_sentence")).values()
    context = {
        "media_url": get_media_url(request),
        "sentences": sentences,
        "id": 1,
        "sections": get_sections(request),
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
    context = {
        "sections": get_sections(request),
        "form": form,
    }
    return HttpResponse(template.render(context, request))


def view_section(request, id):
    if request.user.id != Section.objects.get(id=id).username.id:
        return HttpResponseRedirect('/')
    template = loader.get_template("section.html")
    sentences = Paragraph.objects.filter(section=Section.objects.get(id=id)).values()
    context = {
        "media_url": get_media_url(request),
        "sentences": sentences,
        "id": id,
        "sections": get_sections(request),
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
    current_section_name = Section.objects.get(id=id).section_name
    context = {
        "media_url": get_media_url(request),
        "id": id,
        "sections": get_sections(request),
        "current_section_name": current_section_name,
        "form": form,
    }
    return HttpResponse(template.render(context, request))


def edit_sentence(request, id):
    template = loader.get_template("edit_sentence.html")
    paragraph = Paragraph.objects.get(id=id)
    if request.user.id != paragraph.section.username.id:
        return HttpResponseRedirect('/')
    context = {
        "media_url": get_media_url(request),
        "id": id,
        "sections": get_sections(request),
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
    section = Section.objects.get(id=id)
    if request.user.id != section.username.id:
        return HttpResponseRedirect('/')
    context = {
        "media_url": get_media_url(request),
        "id": id,
        "sections": get_sections(request),
        "section": section,
    }
    return HttpResponse(template.render(context, request))


def update_section(request):
    section = Section.objects.get(id=request.POST['id'])
    section.section_name = request.POST["section_name"]
    section.save()
    return HttpResponseRedirect(reverse('view_section', args=[section.id]))


def error(request, exception):
    return HttpResponseRedirect('/')