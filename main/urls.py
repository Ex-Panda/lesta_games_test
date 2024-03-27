from django.urls import path

from main.apps import MainConfig
from main.views import FileFieldFormView

app_name = MainConfig.name

urlpatterns = [
    path('', FileFieldFormView.as_view(), name='home'),
]