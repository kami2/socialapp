from django.core.exceptions import ValidationError
from django.contrib import messages

def validate_file_size(value):
    filesize = value.size

    if filesize > 1572864:
        raise ValidationError("The maximum file size that can be uploaded is 1.5MB")
    else:
        return value