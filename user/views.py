from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView

from config import settings


class RegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse(settings.LOGIN_REDIRECT_URL)
