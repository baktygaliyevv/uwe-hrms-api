from ..entities.user import User
import json
from ..settings import Session
from ..utils.responses import error, ok
import hashlib
import secrets 

def signup(request):
    data = json.loads(request.body.decode("utf-8"))
    phone = data.get("phone")
    password = data.get("password")

    salt = secrets.token_hex(16)
    hashed_password = hashlib.sha1((password + salt).encode('utf-8')).hexdigest()

    with Session() as session:
        # Check if the user already exists
        existing_user = session.query(User).filter_by(phone=phone).first()
        if existing_user:
            return error('This user already exists')
        
        new_user = User(phone=phone, hash=hashed_password, salt=salt, role='client')

        session.add(new_user)
    
    return ok()
