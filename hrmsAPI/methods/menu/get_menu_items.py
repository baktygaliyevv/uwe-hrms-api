from ...entities.menu import Menu
from ...entities.menu_category import MenuCategory
from ...entities.product import Product
from ...settings import Session
from ...utils.responses import error, ok

def get_menu_items(request):
    if request.method != 'GET':
        return error(code=405, message="Method not allowed")
    
    with Session() as session:
        try:
            menu_categories = session.query(MenuCategory).all()
            payload = []
            
            for category in menu_categories:
                menus = session.query(Menu).filter_by(menu_category_id=category.id).all()
                menu_data = []
                for menu in menus:
                    products = session.query(Product).join(Menu.products).filter(Menu.id == menu.id).all()
                    product_data = [{
                        "id": prod.id,
                        "name": prod.name,
                        "vegan": bool(prod.vegan),
                        "vegetarian": bool(prod.vegetarian),
                        "gluten_free": bool(prod.gluten_free)
                    } for prod in products]
                    
                    menu_data.append({
                        "id": menu.id,
                        "name": menu.name,
                        "price": menu.price,
                        "products": product_data
                    })
                
                payload.append({
                    "id": category.id,
                    "name": category.name,
                    "items": menu_data
                })
            
            return ok(payload)

        except Exception as e:
            return error(code=500, message=str(e))
