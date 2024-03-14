from ..entities.order import Order
from ..settings import Session
from ..utils.responses import error, ok

def get_orders(request):
    if request.method != 'GET':
        return error(code=405, message="Method not allowed")

    with Session() as session:
        try:
            orders = session.query(Order).all()
            payload = []
            for order in orders:
                promocodes = session.query(Promocode).filter_by(id==order.promocode_id)
                promocode_data = [{
                    "id": promocode.id,
                    "discount": promocode.discount,
                    "valid_till":promocode.valid_till
                } for promocode in promocodes]   

                tables = session.query(Table).filter_by(id==order.table_id)
                table_data=[]
                for table in tables:
                    restaurants = session.query(Restaurant).filter_by(id==table.id)
                    restaurant_data=[{
                        "id": restaurant.id,
                        "city": restaurant.city
                    } for restaurant in restaurants]

                    table_data.append({
                        "id":table.id,
                        "restaurant": restaurant_data,
                        "capacity": table.capacity
                    })
                
                users = session.query(User).filter_by(id==order.user_id)
                user_data=[{
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "role": user.role
                    } for user in users]

                order_items = session.query(OrderMenu).filter_by(id==order.id)
                order_item_data=[]
                for order_item in order_items:

                    items = session.query(Menu).filter_by(id==order_item.id)
                    item_data = []
                    for item in items:

                        categories=session.query(MenuCategory).filter_by(id==item.menu_category_id)
                        category_data=[{
                            "id": category.id,
                            "name": category.name
                        } for category in categories]

                        products=session.query(Product).filter_by(id==item.menu_id)
                        product_data=[{
                            "id": product.id,
                            "name": product.name,
                            "vegan": bool(product.vegan),
                            "vegetarian": bool(product.vegetarian),
                            "gluten_free": bool(product.gluten_free)
                        } for product in products]

                        item_data.append({
                            "item": item.id,
                            "name": item.name,
                            "category": category_data,
                            "price": item.price,
                            "products": product_data
                        })
                    

                    order_item_data.append({
                        "item": item_data,
                        "quantity":order_item.quantity
                    })

                payload.append( {
                "id": order.id,
                "user": user_data,
                "table": table_data,
                "promocode": promocode_data,
                "created_at": order.created_at,
                "completed_at": order.completed_at,
                "items": order_item_data
                })

            return ok(payload)

        except Exception as e:
            return error(code=500, message=str(e))