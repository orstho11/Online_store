# Возвращает профиль авторизованного пользователя
def get_userprofile(request):
    if request.user.is_authenticated:
        user = request.user
        return user
    else:
        return None
