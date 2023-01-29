from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorizedToAccessClient(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        if view.is_management():
            return True
        if request.method in SAFE_METHODS:
            return view.is_sales() or view.is_support_of_event(obj)
        else:
           return view.is_sales_contact(obj)

class IsAuthorizedToAccessContract(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'DELETE' or view.is_support():
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if view.is_management():
            return True
        if request.method in SAFE_METHODS:
            return view.is_sales_contact(obj)
        else:
            if request.method == 'UPDATE':
                return view.is_sales() and request.body == {"status": "signed"}
            return view.is_sales()

class IsAuthorizedToAccessEvent(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if view.is_management():
            return True
        if request.method in SAFE_METHODS:
            return view.is_support_contact()
        else:
            if request.method == 'CREATE':
                return view.is_sales()
            else:
                return view.is_support_contact(obj) and view.is_event_in_progress(obj)

