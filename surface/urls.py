from django.urls import path
from surface import views

urlpatterns = [
    path("", views.home, name="home"),
]