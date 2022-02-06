from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from commonData.models import *
from datetime import date

from .models import *



class SignUpSerializer(serializers.ModelSerializer):
    
    email = serializers.CharField(required=True, help_text="Email Address")
    dob = serializers.DateField(required=True,help_text='date of birth format YYYY-MM-DD')
    address = serializers.CharField(
        max_length=300, required=True, help_text="user address")
    company =serializers.CharField(max_length=300, required=True)
    
    @transaction.atomic
    def create(self , validated_data):
        
        try:
            #First created a record in user table with it's authentication credentials and rest data stored in manager table(as i didn't customized the user table)
            
            data = User.objects.create(username=validated_data['email'], first_name=validated_data['first_name'],
                                       last_name=validated_data['last_name'], email=validated_data['email'], is_active=False)
           
           #To save password and activate account
            data.set_password(validated_data['password'])
            data.is_active=True
            data.is_superuser = True
            data.is_staff = True
            data.save()
            manager = Manager.objects.update_or_create(user=data, defaults={"dob": validated_data['dob'], "company": validated_data['company'], "first_name": validated_data[
                                                     'first_name'], "last_name": validated_data['last_name'], "email": validated_data['email'], "address": validated_data['address'],})
            
            return data
        except Exception as e:
            raise serializers.ValidationError(str(e))

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ['is_staff', 'username', 'last_login', 'is_superuser',
                            'is_active', 'date_joined', 'groups', 'user_permissions']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
        
        

class LoginSerializers(serializers.Serializer):
    username   = serializers.CharField(required=False, help_text="Email Address")
    password   = serializers.CharField(required=False)
    
    

############# Subscription Serializer #############

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
        
        


class BookSubscriptionPOSTSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # A booking record will be created with subscription(subscription id) selected by the user
        data = BookSubscription.objects.create(subscription=validated_data['subscription'],
                                        created_by=validated_data['created_by'])
        
        # subscription status and payment status will be default value i.e Cancel and Failed respectivly(it will change after successfull completion of payment.)
        data.save()
        return data

    class Meta:
        model = BookSubscription
        fields = '__all__'
        read_only_fields = ['status', 'payment_status', 'created_at','order_id','razorpay_payment_id']
        
        
        
############# Payment Gateway #################


class ManagerOrderSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField(required=True)
    
    
class ManagerTransactionSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField(required=True)
    razorpay_payment_id = serializers.CharField(required=True)
    
    
########## Subscription Status Change #############

class SubscriptionStatusSerializer(serializers.Serializer):
    status = serializers.CharField(required=True,help_text="Cancel/Active")
    booking_id = serializers.CharField(required=True)