from .models import User
from django.core.exceptions import ObjectDoesNotExist


def check_user(phone):
    try:
        User.objects.get(phone_number=phone)
        return True
    except ObjectDoesNotExist:
        return False


def check_collaborator(phone):
    try:
        user = User.objects.get(phone_number=phone)
        if user.is_collaborator:
            return True
        else:
            return False
    except ObjectDoesNotExist:
        return False
   

def check_user_db():
    return User.objects.all().exists()
