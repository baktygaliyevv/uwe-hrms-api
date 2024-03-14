from ...entities.user import User
from ...settings import Session
from ...utils.responses import error, ok

def get_all_users(request):
    if request.method != "GET":
        return error(code=405, message="Method not allowed")
    
    with Session() as session:
        try:
            users = session.query(User).all()
            users_data = [{
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email, 
                "role": user.role
            } for user in users]

            return ok(users_data)
        
        except Exception as e:
            return error(code=500, message=str(e))