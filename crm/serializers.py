from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
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
            'event_date',
            'support_contact',
            'status',
        ]

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

