from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorizedToAccessClient(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return view.is_sales() or view.is_management()
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return False
        if view.is_management():
            return True
        if request.method in SAFE_METHODS:
            return view.is_sales() or view.is_support_of_event(obj)
        
        return view.is_sales_contact(obj)

class IsAuthorizedToAccessContract(BasePermission):

    def has_permission(self, request, view):
            return view.is_sales() or view.is_management()

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return False
        if view.is_management():
            return True
        if request.method in SAFE_METHODS:
            return view.is_sales_contact(obj)
        else:
            if request.method in ['PUT', 'PATCH']:
                return view.is_sales() and request.data == {'status': True}
            return view.is_sales()

class IsAuthorizedToAccessEvent(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
                return view.is_sales() or view.is_management()
        return view.is_support() or view.is_management()

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return False
        if view.is_management():
            return True
        if request.method in SAFE_METHODS:
            return view.is_support_contact()
        else:
            return view.is_support_contact(obj) and view.is_event_in_progress(obj)

