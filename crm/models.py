from django.db import models

from authentication.models import User
from django.conf import settings


class Client(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(null=False, unique=True)
    phone = models.CharField(max_length=20, unique=True, null=False)
    mobile = models.CharField(max_length=20, unique=True, null=False)
    company_name = models.CharField(max_length=250, null=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clients'
    )
    def __str__(self):
        return f"Client: {self.first_name} {self.last_name} - Company: {self.company_name}"


class Contract(models.Model):
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    amount = models.FloatField()
    status = models.BooleanField(default=False, verbose_name='signed')
    payment_due = models.DateField(null=True)
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='contracts'
    )
    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, null=False, related_name='contracts'
    )

    def __str__(self):
        return f"""Amount: {self.amount} - 
        Signed: {self.status} - 
        Client: {self.client} - 
        Sales contact: {self.sales_contact} - 
        Payment due: {self.payment_due} - 
        Date created: {self.date_created}"""


class Event(models.Model):
    IN_PROGRESS = 'In progress'
    DONE = 'Done'

    STATUS_CHOICES = (
        (IN_PROGRESS, 'In progress'),
        (DONE, 'Done'),
    )

    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    attendees = models.IntegerField()
    notes = models.TextField()
    client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, null=False, related_name='events'
    )
    event_date = models.DateTimeField()
    support_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='events'
    )
    event_status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=IN_PROGRESS)

    def __str__(self):
        return f"""
        Event date: {self.event_date} - 
        status: {self.event_status} - 
        Client: {self.client} - 
        Support contact: {self.support_contact} - 
        Attendees: {self.attendees} - 
        Date created: {self.date_created}"""