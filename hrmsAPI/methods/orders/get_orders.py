# from ...entities.order import Order
# from ...entities.promocode import  Promocode
# from ...entities.table import Table
# from ...entities.restaurant import Restaurant
# from ...entities.user import User
# from ...entities.order_menu import OrderMenu
# from ...entities.menu import Menu
# from ...entities.menu_category import MenuCategory
# from ...entities.product import Product
# from ...entities.menu_product import t_menu_products

# from ...settings import Session
# from ...utils.responses import error, ok

# def get_orders(request):
#     if request.method != 'GET':
#         return error(code=405, message="Method not allowed")

#     with Session() as session:
#         try:
#             orders = session.query(Order).all()
#             payload = []
#             for order in orders:
#                 promocode = session.query(Promocode).get(order.promocode_id)
#                 promocode_data = {
#                     "id": promocode.id,
#                     "discount": promocode.discount,
#                     "valid_till":promocode.valid_till
#                 }   

#                 table = session.query(Table).get(order.table_id)
#                 restaurant = session.query(Restaurant).get(table.restaurant_id)
#                 restaurant_data={
#                     "id": restaurant.id,
#                     "city": restaurant.city
#                 }
#                 table_data={
#                     "id":table.id,
#                     "restaurant": restaurant_data,
#                     "capacity": table.capacity
#                 }
                
#                 user = session.query(User).get(order.user_id)
#                 user_data={
#                     "id": user.id,
#                     "first_name": user.first_name,
#                     "last_name": user.last_name,
#                     "email": user.email,
#                     "role": user.role
#                     }

#                 order_items = session.query(OrderMenu).filter_by(id=order.id)
#                 order_item_data=[]
#                 for order_item in order_items:

#                     item = session.query(Menu).get(order_item.id)

#                     category = session.query(MenuCategory).get(item.menu_category_id)
#                     category_data={
#                         "id": category.id,
#                         "name": category.name
#                     }

#                     menu_products_ids=session.query(t_menu_products).filter_by(menu_id=item.id)
#                     products=session.query(Product).filter(Product.id.in_([product_id.product_id for product_id in menu_products_ids]))
#                     product_data=[{
#                         "id": product.id,
#                         "name": product.name,
#                         "vegan": bool(product.vegan),
#                         "vegetarian": bool(product.vegetarian),
#                         "gluten_free": bool(product.gluten_free)
#                     } for product in products]

#                     item_data={
#                         "item": item.id,
#                         "name": item.name,
#                         "category": category_data,
#                         "price": item.price,
#                         "products": product_data
#                     }
                    

#                     order_item_data.append({
#                         "item": item_data,
#                         "quantity":order_item.quantity
#                     })

#                 payload.append( {
#                 "id": order.id,
#                 "user": user_data,
#                 "table": table_data,
#                 "promocode": promocode_data,
#                 "created_at": order.created_at,
#                 "completed_at": order.completed_at,
#                 "items": order_item_data
#                 })

#             return ok(payload)

#         except Exception as e:
#             return error(code=500, message=str(e))