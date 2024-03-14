from ...entities.user import User
from ...settings import Session
from ...utils.responses import error, ok
import json
import secrets
import hashlib

def add_user(request):
    if request.method != "POST":
        return error(code=405, message="Method not allowed")
    
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return error(code=400, message="Invalid JSON")
    
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not all([first_name, last_name, email, password, role]):
        return error(code=400, message="Missing data")
    
    salt = secrets.token_hex(16)
    hashed_password = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
    
    with Session() as session:
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            return error(code=400, message="User with this email address already exists")
        
        new_user = User(
            first_name = first_name,
            last_name = last_name,
            email = email,
            hash = hashed_password,
            salt = salt,
            role = role,
            verified = 1
        )

        try:
            session.add(new_user)
            session.commit()
            
        except Exception as e:
            session.rollback()
            return error(code=500, message=str(e))
        
        return ok({
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "role": new_user.role,
            "verified": new_user.verified
        })