from django.http import JsonResponse
from django.urls import resolve
from django.utils.timezone import now
from ..models import UserTokens

def unauthorized_response(message):
    response = JsonResponse({'detail': message})
    response.status_code = 401
    return response

def auth_middleware(get_response):
    def middleware(request):
        url_name = resolve(request.path_info).url_name
        open_paths = ['auth-login', 'auth-signup', 'auth-verify', 'get-restaurants', 'get-tables', 'get-menu-item', 'get-menu-categories', 'get-add-client-order', 'get-add-client-delivery', 'get-specific-promocode']

        if url_name in open_paths:
            return get_response(request)

        protected_paths = {
            'get-users': ['admin'],  
            'add-users': ['admin'],  
            'edit-user': ['admin'],  
            'delete-user': ['admin'],  

            'add-menu-item': ['admin'], 
            'edit-menu-item': ['admin'], 
            'delete-menu-item': ['admin'], 
            'add-menu-product': ['admin'], 
            'delete-menu-product': ['admin'], 
            'add-menu-category': ['admin'], 

            'get-products': ['admin', 'manager'], 
            'add-product': ['admin'], 
            'edit-product': ['admin'], 
            'delete-product': ['admin'],  

            'get-promocodes': ['admin', 'manager'],  
            'add-promocode': ['admin', 'manager'],  
            'delete-promocode': ['admin', 'manager'],  

            'add-tables': ['admin', 'manager'], 
            'edit-delete-table': ['admin', 'manager'],  

            'get-orders': ['admin', 'manager', 'staff', 'chef'],
            'add-orders': ['admin', 'manager', 'staff', 'chef'],
            'edit-delete-order': ['admin', 'manager', 'staff', 'chef'],
            'add-order-menu-items': ['admin', 'manager', 'staff', 'chef'],
            'edit-order-menu-item': ['admin', 'manager', 'staff', 'chef'],
            'delete-order-menu-item': ['admin', 'manager', 'staff', 'chef'],

            'delete-restaurant': ['admin'],  

            'get-add-delivery': ['admin', 'manager', 'staff', 'chef'],
            'edit-delete-delivery': ['admin', 'manager', 'staff', 'chef'],
        }

        token = request.COOKIES.get('token')
        if not token:
            return unauthorized_response("Token is missing")

        try:
            user_token = UserTokens.objects.get(token=token)
            if user_token.expiration_date < now():
                return unauthorized_response("Token has expired")
            
            user = user_token.user
            if url_name in protected_paths:
                if user.role not in protected_paths[url_name]:
                    return unauthorized_response("Unauthorized")

            request.user = user

        except UserTokens.DoesNotExist:
            return unauthorized_response("Invalid token")
        
        return get_response(request)

    return middleware
