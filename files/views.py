from django.http import JsonResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponse
from django.views import View
from django.views.generic import ListView
from encryption.aes_utils import generate_key, encrypt_file, encode_key, decrypt_file, decode_key
import os
from .models import File
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import logging
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
import mimetypes
from django.contrib.auth.forms import UserCreationForm
from .forms import ShareFileForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q, Value, CharField, F
from .utils import generate_presigned_url
import boto3
from botocore.exceptions import ClientError
from django.contrib import messages

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(View):
    def get(self, request):
        return render(request, 'files/upload.html')

    def post(self, request):
        file = request.FILES.get('file')
        file_type = file.content_type if file else None  # Determine the file type

        file_record = File.objects.create(
            user=request.user,
            name=file.name,
            file=file,
            file_type=file_type  # Ensure this matches the field in the model
        )

        return render(request, 'files/upload.html', {
            'success': f'Upload complete! File "{file_record.name}" has been uploaded successfully.'
        })

class FileDownloadView(View):
    def get(self, request, file_id):
        try:
            # Check if the file belongs to the user or is shared with the user
            file_record = File.objects.filter(
                Q(id=file_id) & (Q(user=request.user) | Q(shared_with=request.user))
            ).first()

            if not file_record:
                raise Http404("File not found.")

            # Generate a presigned URL for the file
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': file_record.file.name,
                },
                ExpiresIn=3600  # URL expires in 1 hour
            )

            # Use FileResponse to force download
            response = FileResponse(
                s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_record.file.name)['Body'],
                as_attachment=True,
                filename=file_record.name
            )
            return response

        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            raise Http404("File not found.")

@method_decorator(login_required, name='dispatch')
class FileListView(ListView):
    model = File
    template_name = 'files/file_list.html'
    context_object_name = 'files'

    def get_queryset(self):
        # Files owned by the user
        owned_files = File.objects.filter(user=self.request.user).annotate(shared_by=Value('You', output_field=CharField()))
        
        # Files shared with the user
        shared_files = File.objects.filter(shared_with=self.request.user).annotate(shared_by=F('user__username'))

        # Combine both querysets
        return owned_files.union(shared_files)

class FileDeleteView(View):
    def post(self, request, file_id):
        try:
            # Ensure the file belongs to the logged-in user
            file_record = File.objects.get(id=file_id, user=request.user)
            file_record.delete()
            return HttpResponseRedirect(reverse('file_list'))
        except File.DoesNotExist:
            raise Http404("File not found.")

@login_required
def share_file(request, file_id):
    file_record = get_object_or_404(File, id=file_id, user=request.user)
    if request.method == 'POST':
        form = ShareFileForm(request.POST, user=request.user)
        if form.is_valid():
            user_to_share = form.cleaned_data['user']
            message = form.cleaned_data['message']
            file_record.shared_with.add(user_to_share)
            return redirect('file_list')
    else:
        form = ShareFileForm(user=request.user)
    return render(request, 'files/share_file.html', {'form': form, 'file': file_record})

def home(request):
    return render(request, 'files/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile  # Import the UserProfile model

@login_required
def profile(request):
    return render(request, 'files/profile.html', {'user': request.user})

@login_required
def manage_friends(request):
    # Ensure the user has a profile
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        friend_id = request.POST.get('friend_id')
        friend = get_object_or_404(User, id=friend_id)

        if action == 'add':
            profile.friends.add(friend.profile)
            messages.success(request, f'{friend.username} has been added as a friend.')
        elif action == 'remove':
            profile.friends.remove(friend.profile)
            messages.success(request, f'{friend.username} has been removed from your friends.')
        elif action == 'send_file':
            file_id = request.POST.get('file_id')
            file_record = get_object_or_404(File, id=file_id, user=request.user)
            file_record.shared_with.add(friend)
            messages.success(request, f'File "{file_record.name}" has been successfully sent to {friend.username}.')
            return redirect('manage_friends')

        return redirect('manage_friends')

    all_users = User.objects.exclude(id=request.user.id)
    friends = profile.friends.all()
    user_files = File.objects.filter(user=request.user)  # Get files uploaded by the user
    return render(request, 'files/manage_friends.html', {
        'all_users': all_users,
        'friends': friends,
        'user_files': user_files,
    })