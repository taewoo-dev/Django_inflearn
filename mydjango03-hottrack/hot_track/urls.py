from django.urls import path, re_path
from . import views

urlpatterns = [
    path(route="", view=views.index),
    path(route="<int:pk>/cover.png", view=views.cover_png),
    re_path(
        route=r"^export\.(?P<format>(csv|xlsx))$", view=views.export, name="export"
    ),
]
