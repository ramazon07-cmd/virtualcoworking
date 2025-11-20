from django.urls import path
from . import views

urlpatterns = [
    path('files/', views.file_list, name='file_list'),
    path('files/upload/', views.upload_file, name='upload_file'),
    path('files/<int:file_id>/download/', views.download_file, name='download_file'),
    path('files/<int:file_id>/delete/', views.delete_file, name='delete_file'),
    path('notes/', views.note_list, name='note_list'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('notes/<int:note_id>/update/', views.update_note, name='update_note'),
    path('notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
]