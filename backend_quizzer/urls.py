from django.urls import path
from . import views


urlpatterns = [
    path("upload_file", views.upload_file),
    path("delete_file/<int:id>", views.delete_file),
    path("update_file", views.update_file),
    path("view_file/<int:id>", views.view_file),
    path("view_files", views.view_files)
]
