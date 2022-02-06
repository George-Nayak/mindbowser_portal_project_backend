from django.contrib import admin
from nested_admin import NestedModelAdmin
from .models import *

# Register your models here.
@admin.register(Subscription)
class SubscriptionAdmin(NestedModelAdmin):
    model = Subscription
    list_display = ['id', 'plan_name',  'plan_range', 'amount',  'created_at', 'updated_at']