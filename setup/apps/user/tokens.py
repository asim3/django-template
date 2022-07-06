from rest_framework_simplejwt.tokens import RefreshToken


class CustomizedRefreshToken(RefreshToken):

    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token["username"] = user.get_username()
        token["short_name"] = user.get_short_name()
        token["full_name"] = user.get_full_name()
        token["permissions"] = user.get_permissions_as_str()
        return token
