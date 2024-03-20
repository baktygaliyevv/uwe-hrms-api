from ...entities.delivery import Delivery
from ...settings import Session
from ...utils.responses import error, ok
import json

def add_item_to_delivery(request):
    if request.method != "POST":
        return error(code=405, message="Method not allowed")
    
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return error(code=400, message="Invalid JSON")
    
    id = data.get("id")
    user_id = data.get("user_id")
    restaurant_id = data.get("restaurant_id")
    promocode_id = data.get("promocode_id")
    address = data.get("address")
    created_at = data.get("created_at")
    status = data.get("status")

    if not all([id, user_id, restaurant_id, promocode_id,
                 address, created_at, status]):
        return error(code=400, message="Missing data")
    
    with Session() as session:
        existing_delivery = session.query(Delivery).filter_by(id=id).first()
        if existing_delivery:
            return error(code=400, message="Delivery with this ID already exists")

        new_delivery = Delivery(
            id = id,
            user_id = user_id,
            restaurant_id = restaurant_id,
            promocode_id = promocode_id,
            address = address,
            created_at = created_at,
            status = status
        )

        try:
            session.add(new_delivery)
            session.commit()

        except Exception as e:
            session.rollback()
            return error(code=500, message=str(e))
        
        return ok({
            "id": new_delivery.id,
            "user_id": new_delivery.user_id,
            "restaurant_id": new_delivery.restaurant_id,
            "promocode_id": new_delivery.promocode_id,
            "address": new_delivery.address,
            "created_at": new_delivery.created_at,
            "status": new_delivery.status
        })