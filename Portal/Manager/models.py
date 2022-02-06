from django.db import models

from django.contrib.auth.models import User
from commonData.models import *




# Create your models here.
class Manager(models.Model):
    """ Register Manager details reside here """
   
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(
        max_length=100, null=True, help_text="user first name")
    last_name = models.CharField(
        max_length=100, null=True, help_text="user last name", blank=True)

    email = models.CharField(max_length=100, null=True, help_text="user email")
    address = models.CharField(
        max_length=400, null=True, blank=True, help_text="user address")
    dob = models.DateField(
        blank=True, null=True, help_text='date of birth format YYYY-MM-DD', verbose_name='date of birth')
    company = models.CharField(max_length=100, null=True,
                              help_text="user company name", unique=True) 
    is_deleted = models.BooleanField(
        default=False, help_text="activate/deactivate user")

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{}-{}-{}".format(self.pk, self.email, self.first_name)

    class Meta:
        unique_together = ('user', 'email')
        verbose_name_plural = "Managers"
        db_table = 'manager'


class BookSubscription(models.Model):
    """
    Subscription Booking Details
    """
    STATUS_CHOICE = (
        ("Cancel", "Cancel"),
        ("Active", "Active"),
        
    )
    PAYMENT_STATUS_CHOICES = (
        ('F', 'Failed'),
        ('S', 'Success'),
    )
   
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20,default=STATUS_CHOICE[0][0] ,choices=STATUS_CHOICE,
                              blank=True, null=True, help_text="Status of the Plan")
    order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(
        Manager, on_delete=models.CASCADE, blank=True, null=True)
    payment_status = models.CharField(
        max_length=10, default=PAYMENT_STATUS_CHOICES[0][0], choices=PAYMENT_STATUS_CHOICES, blank=True, null=True, help_text="Payment Status")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "{}-{}-{}".format(self.id, self.subscription,self.created_by)

    class Meta:
        verbose_name_plural = "Book Subscription"
        db_table = "book_subscription"
