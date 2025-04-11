from django.urls import path

from apps.settings.views import SettingsRetrieveUpdateView

urlpatterns = [
    path("settings/", SettingsRetrieveUpdateView.as_view(), name='settings'),
]
