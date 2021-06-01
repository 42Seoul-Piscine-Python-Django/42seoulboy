from django.conf import settings
import jwt


def get_moviemon_token(moviemon_id):
    return jwt.encode({"id": moviemon_id}, settings.SECRET_KEY, algorithm="HS256")


def get_moviemonid(token):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return data['id']
    except:
        return None
