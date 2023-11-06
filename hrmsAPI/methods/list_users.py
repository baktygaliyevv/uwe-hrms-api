from django.http import JsonResponse
from django.views import View
from ..settings import Session
from datetime import datetime
from ..entities.user import User
from ..entities.user_tokens import UserToken

class ListUsers(View):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get('token')
        if not token:
            return JsonResponse({"status": "Error", "message": "Token is missing"}, status=401)

        with Session() as session:
            user_token = session.query(UserToken).filter_by(token=token).first()
            if not user_token or user_token.expiration_date < datetime.now():
                return JsonResponse({"status": "Error", "message": "Unauthorized"}, status=401)
            
            user = session.query(User).get(user_token.user_id)
            if user is None or user.role not in ['manager', 'admin']:
                return JsonResponse({"status": "Error", "message": "Unauthorized"}, status=401)
            
            # if user is authorized, proceed to get the list of users
            users = session.query(User).all()
            users_list = [
                {
                    "id": user.id,
                    "name": user.name,
                    "phone": user.phone,
                    "role": user.role
                } for user in users
            ]

            return JsonResponse({
                "status": "Ok",
                "response": {
                    "users": users_list
                }
            }, status=200)
