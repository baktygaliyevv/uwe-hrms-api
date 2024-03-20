from ...entities.delivery import Delivery
from ...settings import Session
from ...utils.responses import error, ok
import json

def delete_delivery(request):
    if request.method != "DELETE":
        return error(code=405, message="Method not allowed")
    
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return error(code=400, message="Invalid JSON")
    
    id = data.get("id")
    
    if not id:
        return error(code=400, message="Missing delivery ID")
    
    with Session() as session:
        existing_delivery = session.query(Delivery).filter_by(id=id).first()
        if not existing_delivery:
            return error(code=404, message="Delivery not found")
        
        try:
            session.delete(existing_delivery)
            session.commit()

        except Exception as e:
            session.rollback()
            return error(code=500, message=str(e))
        
        return ok({"message": "Delivery deleted successfully"})
