from sqlalchemy.orm import sessionmaker
from .entities.user import User
from sqlalchemy import create_engine
import json
from django.http import JsonResponse
from settings import Session
from .utils.responses import error, ok

def signup(request):
    data = json.loads(request.body.decode("utf-8"))
    phone = data.get("phone")
    password = data.get("password")

    with Session() as session:
        # Check if the user already exists
        existing_user = session.query(User).filter_by(phone=phone).first()
        if existing_user:
            return error('This user already exists')
        
        new_user = User(phone=phone, password=password, role='client')

        session.add(new_user)
    
    return ok
