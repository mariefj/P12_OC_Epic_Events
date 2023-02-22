import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Client, Contract, Event
from .serializers import ClientListSerializer, ClientDetailSerializer, ContractSerializer, EventSerializer
from .permissions import IsAuthorizedToAccessClient, IsAuthorizedToAccessContract, IsAuthorizedToAccessEvent


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

class RoleMixin:

    def is_sales(self):
        return self.request.user.role == "Sales"

    def is_support(self):
        return self.request.user.role == "Support"

    def is_management(self):
        return self.request.user.role == "Management"

    def is_support_of_event(self, obj):
        events =  Event.objects.filter(client=obj)
        support_contacts = [event.support_contact for event in events]
        return self.request.user.role == 'Support' and self.request.user in support_contacts

class IsSalesContactMixin:

    def is_sales_contact(self, obj):
        return self.request.user.role == 'Sales' and obj.sales_contact == self.request.user

class ClientViewSet(MultipleSerializerMixin, RoleMixin, IsSalesContactMixin, ModelViewSet):

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedToAccessClient]
    filter_backends = [SearchFilter]
    search_fields = ['last_name', 'email']

    def get_queryset(self):
        role = self.request.user.role
        if role == "Support":
            events = self.request.user.events.all()
            return Client.objects.filter(events__in=events)
        if role == 'Sales':
            return self.request.user.clients.all()
        if role == 'Management':
            return Client.objects.all()


class ContractViewSet(MultipleSerializerMixin, RoleMixin, IsSalesContactMixin, ModelViewSet):
    
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedToAccessContract]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['client__last_name', 'client__email', 'amount', 'date_created']
    ordering_fields = ['payment_due']

    def get_queryset(self):
        role = self.request.user.role
        if role == 'Sales':
            return self.request.user.contracts.all()
        if role == 'Management':
            return Contract.objects.all()


class EventViewSet(ModelViewSet, RoleMixin):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedToAccessEvent]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['client__last_name', 'client__email', 'event_date']
    ordering_fields = ['event_date']

    def get_queryset(self):
        role = self.request.user.role
        if role == "Support":
            return self.request.user.events.all()
        if role == 'Management':
            return Event.objects.all()

    def is_support_contact(self, obj):
        return obj.support_contact == self.request.user

    def is_event_in_progress(self, obj):
        return obj.event_status == 'In progress'

