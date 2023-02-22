from django.contrib import admin

from authentication.models import User
from .models import Client, Contract, Event

admin.site.disable_action('delete_selected')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'sales_contact':
            kwargs["queryset"] = User.objects.filter(role="Sales")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    model = Contract
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'sales_contact':
            kwargs["queryset"] = User.objects.filter(role="Sales")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'support_contact':
            kwargs["queryset"] = User.objects.filter(role="Support")
        if db_field.name == 'contract':
            kwargs["queryset"] = Contract.objects.filter(status=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



