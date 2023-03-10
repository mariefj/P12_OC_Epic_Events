from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)

from authentication.models import User
from .models import Client, Contract, Event


class ContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            'id',
            'date_created',
            'date_updated',
            'amount',
            'status',
            'payment_due',
            'sales_contact',
            'client',
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'date_created',
            'date_updated',
            'attendees',
            'notes',
            'client',
            'contract',
            'event_date',
            'support_contact',
            'event_status',
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']
    
    def validate_support_contact(self, value):
        user = User.objects.filter(id=value.id)[0]
        if not user or user.role != 'Support':
            raise ValidationError('Support contact must be a support user')
        return value

    def validate_contract(self, value):
        contract = Contract.objects.filter(id=value.id)[0]
        if not contract or contract.status != 1:
            raise ValidationError('Contract must be signed')
        return value

class ClientListSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
            'date_created',
            'date_updated',
            'sales_contact',
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

    def validate_sales_contact(self, value):
        user = User.objects.filter(id=value.id)[0]
        if not user or user.role != 'Sales':
            raise ValidationError('Sales contact must be a sales user')
        return value


class ClientDetailSerializer(ModelSerializer):

    def get_contracts(self, instance):
        queryset = instance.contracts
        serializer = ContractSerializer(queryset, many=True)
        return serializer.data

    def get_events(self, instance):
        queryset = instance.events
        serializer = EventSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
            'date_created',
            'date_updated',
            'sales_contact',
            'contracts',
            'events',
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']


