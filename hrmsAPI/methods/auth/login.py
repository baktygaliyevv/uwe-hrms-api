from ..entities.user import User
from ..entities.user_tokens import UserToken
import json
from ..settings import Session
from ..utils.responses import error, ok
import hashlib
import secrets
from datetime import datetime, timedelta

def login(request):
    data = json.loads(request.body.decode("utf-8"))
    phone = data.get("phone")
    password = data.get("password")

    with Session() as session:
        # Fetch the user based on the phone
        user = session.query(User).filter_by(phone=phone).first()
        
        # If no user or the passwords don't match
        if not user or user.hash != hashlib.sha1((password + user.salt).encode('utf-8')).hexdigest():
            return error(code=401, message="Incorrect phone number or password.")

        token = secrets.token_hex(32)
        expiration_duration = 60 # 60 days
        expiration_date = datetime.now() + timedelta(days=expiration_duration)

        user_token = UserToken(user_id=user.id, token=token, expiration_date=expiration_date)
        session.add(user_token)

        role_hierarchy = ['client', 'courier', 'staff', 'chef', 'manager', 'admin']
        user_roles = {role: False for role in role_hierarchy}

        for index, role in enumerate(role_hierarchy):
            if user.role == role:
                for i in range(index + 1):
                    user_roles[role_hierarchy[i]] = True
                break

        response = ok({
            "role": user_roles
        })

        # Set the token in the cookie of the response
        response.set_cookie(key="token", value=token, expiration_date=expiration_date)

        return response
