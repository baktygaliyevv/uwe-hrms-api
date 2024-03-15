from datetime import datetime
from ..settings import Session
from ..entities.user_tokens import UserToken
from ..utils.responses import error

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of paths that should skip the token check
        open_paths = [
            '/schema',  
            '/schema/swagger-ui',  
            '/schema/redoc',  
            '/ping',
            '/login',
            '/signup',
        ]

        if request.path.rstrip('/') in open_paths:
            return self.get_response(request)

        token = request.COOKIES.get('token')
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
