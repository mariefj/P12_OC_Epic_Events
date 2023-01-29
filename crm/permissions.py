from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Client, Contract, Event


class IsAuthorizedToAccessClient(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
                return False
        if view.isManagement():
            return True

        if request.method in SAFE_METHODS:
            return view.isSales() or view.isSupportOfEvent(obj)
        else:
           return view.isSalesContact(obj)


class IsAuthorizedToAccessClientOrContract(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.role == 'Sales' or request.user.role == 'Support'
        else:
            return request.user.role == 'Sales'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return obj.sales_contact == request.user


class IsAuthorizedSalesOrAssignedSupportToManageEvents(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'PUT':
            return request.user.role == 'Sales' or request.user.role == 'Support'
        else:
            return request.user.role == 'Sales'

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        else:
            return bool((obj.support_contact == request.user and obj.event_status == 'In progress') or obj.client.sales_contact == request.user)



# class IsManagement(BasePermission):
#     """
#     Permission for users in the management group.
#     """
#     def has_permission(self, request, view):
#         return request.user.role == 'Management'

#     def has_object_permission(self, request, view, obj):
#         return request.user.role == 'Management'

# class IsSales(BasePermission):
#     """
#     Permission for users in the sales group.
#     """
#     def has_permission(self, request, view):
#         return request.user.role == 'Sales'

#     def has_object_permission(self, request, view, obj):
#         if isinstance(obj, Client):
#             return obj.sales_contact == request.user
#         elif isinstance(obj, Contract):
#             return obj.sales_contact == request.user
#         return request.user.role == 'Sales'

# class IsSupport(BasePermission):
#     """
#     Permission for users in the support group.
#     """
#     def has_permission(self, request, view):
#         return request.user.role == 'Support'

#     def has_object_permission(self, request, view, obj):
#         if isinstance(obj, Event):
#             return obj.support_contact == request.user and obj.event_status == 'In progress'
#         elif isinstance(obj, Client):
#             return obj.event_set.filter(support_contact=request.user).exists()
#         return request.user.role == 'Support'
