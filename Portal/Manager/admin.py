from django.contrib import admin

from nested_admin import NestedModelAdmin

from .models import *

# Register your models here.



@admin.register(Manager)
class ManagerAdmin(NestedModelAdmin):
    model = Manager
    list_display = ['id', 'user', 'first_name',  'last_name', 'email', 'address', 'company', 'dob', 'is_deleted',  'created_at', 'updated_at']


@admin.register(BookSubscription)
class BookSubscriptionAdmin(NestedModelAdmin):
    model = BookSubscription
    list_display = ['id', 'subscription', 'status',  'payment_status', 'created_by',  'created_at']