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
        support_contacts = Event.objects.filter(client=obj).support_contact
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
        clients = Client.objects.all()
        if self.request.user.role == "Support":
            events = Event.objects.filter(support_contact=self.request.user)
            clients_support = []
            for event in events:
                if event.support_contact == self.request.user:
                    clients_support.append(event.client.pk)
            return Client.objects.filter(id__in=clients_support)
        return clients

    def perform_create(self, serializer):
        serializer.save(sales_contact=self.request.user)


class ContractViewSet(MultipleSerializerMixin, RoleMixin, IsSalesContactMixin, ModelViewSet):
    
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedToAccessContract]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['client__last_name', 'client__email', 'amount', 'date_created']
    ordering_fields = ['payment_due']

    def get_queryset(self):
        contracts = Contract.objects.all()
        if self.request.user.role == "Support":
            events = Event.objects.filter(support_contact=self.request.user)
            contracts_support = [event.contract.pk for event in events]
            return Contract.objects.filter(id__in=contracts_support)
        return contracts

    def perform_create(self, serializer):
        serializer.save(sales_contact=self.request.user)


class EventViewSet(ModelViewSet, RoleMixin):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedToAccessEvent]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['client__last_name', 'client__email', 'event_date']
    ordering_fields = ['event_date']

    def get_queryset(self):
        events = Event.objects.all()
        if self.request.user.role == 'Support':
            return Event.objects.filter(support_contact=self.request.user.id)
        return events

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        contract_id = request.data['contract']
        contract = Contract.objects.get(pk=contract_id)
        client = Client.objects.get(pk=contract.client.id)
        request.data["client"] = client.pk
        return super().create(request, *args, **kwargs)

    def is_support_contact(self, obj):
        return obj.support_contact == self.request.user

    def is_event_in_progress(self, obj):
        return obj.event_status == 'In progress'
