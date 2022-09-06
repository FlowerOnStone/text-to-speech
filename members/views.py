from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Members
from .forms import RegistrationmForm


# Create your views here.
def register(request):
    form = RegistrationmForm()
    if request.method == 'POST':
        form = RegistrationmForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    template = loader.get_template('register.html')
    return HttpResponse(template.render({"form": form}, request))
