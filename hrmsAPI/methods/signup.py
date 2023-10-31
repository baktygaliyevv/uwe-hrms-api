from sqlalchemy.orm import sessionmaker
from .entities.user import User
from sqlalchemy import create_engine
import json
from django.http import JsonResponse
from settings import Session

def signup(request):
    data = json.loads(request.body.decode("utf-8"))
    phone = data.get("phone")
    password = data.get("password")

    # Create a new session
    session = Session()

    # Check if the user already exists
    existing_user = session.query(User).filter_by(phone=phone).first()
    if existing_user:
        session.close()
        return JsonResponse({'status': 'Error', 'message': 'This user already exists.'}, status=400)

    # Create a new user with the 'client' role by default
    new_user = User(phone=phone, password=password, role='client')

    session.add(new_user)
    session.commit()
    
    # Close the session
    session.close()

    return JsonResponse({'status': 'Ok'}, status=200)
