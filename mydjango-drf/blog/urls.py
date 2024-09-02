from django.urls import path, include
from . import views
from . import api

urlpatterns = []

urlpatterns_api_v1 = [
    path(route="", view=api.post_list, name="post_list"),
    path(route="<int:pk>/", view=api.post_detail, name="post_detail"),
    path(route="new/", view=api.post_new, name="post_new"),
    path(route="<int:pk>/edit/", view=api.post_edit, name="post_edit "),
]

urlpatterns += [
    path("api/", include((urlpatterns_api_v1, "api-v1"))),
]
