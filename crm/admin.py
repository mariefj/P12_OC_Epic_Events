from django.contrib import admin

from .models import Client, Contract, Event

admin.site.disable_action('delete_selected')

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)


