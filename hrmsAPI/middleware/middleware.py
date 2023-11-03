from datetime import datetime
from settings import Session
from ..entities.user_tokens import UserToken
from ..utils.responses import error

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        token = request.COOKIES.get('token') # проверка токена перед обработкой запроса
        if not token:
            return error(code=401, message="Token is missing")

        with Session() as session:
            user_token = session.query(UserToken).filter_by(token=token).first()
            if not user_token:
                return error(code=401, message="Invalid token")

            if user_token.expiration_date < datetime.now():
                return error(code=401, message="Token has expired")

        response = self.get_response(request)
        return response
