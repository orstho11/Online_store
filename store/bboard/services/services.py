# Возвращает профиль авторизованного пользователя
from bboard.models import UserProfile
def get_userprofile(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        return user_profile
    else:
        return None
