# from ...entities.menu_category import MenuCategory
# from ...settings import Session
# from ...utils.responses import error, ok

# def get_menu_categories(request):
#     if request.method != 'GET':
#         return error(code=405, message="Method not allowed")

#     with Session() as session:
#         try:
#             categories = session.query(MenuCategory).all()
#             categories_data = [{
#                 "id": category.id,
#                 "name": category.name
#             } for category in categories]

#             return ok(categories_data)

#         except Exception as e:
#             return error(code=500, message=str(e))