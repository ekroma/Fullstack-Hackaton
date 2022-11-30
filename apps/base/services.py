from django.core.exceptions import ValidationError
import os

def get_upload_path_avatar(instance, file):
    return f'avatar/user_{instance.username}/{file}'

def validate_image_size(img):
    mgb_limit = 2
    if img.size > mgb_limit * 1024 * 1024:
        raise ValidationError(f'Max size of avatar is {mgb_limit}MB')

def get_upload_path_album(instance, file):
    return f'album/user_{instance.user.username}/{file}'

def get_upload_path_track(instance, file):
    return f'track/user_{instance.user.username}/{file}'

def delete_old_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
