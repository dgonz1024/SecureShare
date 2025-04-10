from django.urls import path
from .views import FileUploadView, FileListView, FileDownloadView, FileDeleteView, share_file, register, profile, manage_friends

urlpatterns = [
    path('', FileListView.as_view(), name='file_list'),
    path('upload/', FileUploadView.as_view(), name='upload_file'),
    path('delete/<int:file_id>/', FileDeleteView.as_view(), name='delete_file'),
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='download_file'),
    path('share/<int:file_id>/', share_file, name='share_file'),
    path('register/', register, name='register'),  # Add the registration URL
    path('profile/', profile, name='profile'),
    path('friends/', manage_friends, name='manage_friends'),
]