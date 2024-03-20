from ...entities.delivery import Delivery
from ...settings import Session
from ...utils.responses import error, ok

def get_all_delivery(request):
    if request.method != 'GET':
        return error(code=405, message="Method not allowed")
    
    with Session() as session:
        try:
            deliveries = session.query(Delivery).all()
            deliveries_data = [{
                "id": delivery.id,
                "user_id": delivery.user_id,
                "restaurant_id": delivery.restaurant_id,
                "promocode_id": delivery.promocode_id,
                "address": delivery.address,
                "created_at": delivery.created_at,
                "status": delivery.status
            }for delivery in deliveries]

            return ok(deliveries_data)
        
        except Exception as e:
            return error(code=500, message=str(e))  