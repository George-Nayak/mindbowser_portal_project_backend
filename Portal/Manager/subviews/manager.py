from locale import currency
from rest_framework.authtoken.models import Token
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.contrib.auth import login, authenticate
from Manager.serializers import *
from django.contrib.auth.models import User
from utils.api_handle_errors import handle_errors
from commonData.models import *
from decimal import *
import razorpay
import requests



class SignUpAPIView( generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, format=None):

        response = {}
        responsedata = []
        
        # Serialization of data
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['username'] = serializer.validated_data['email']
            
            #To check account exist or not
            if User.objects.filter(username=serializer.validated_data['email']).exists():
                response['message'] = "This email address is already registered"
                response['result'] = 0
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            

            user_object = serializer.save()

            message = 'You have successfully created your account.'

            #result =0 for errors and result =1 for sucess,it's used for data binding in frontend
            #also i have added status of each request in api response
            response['message'] = message
            response['result'] = 1
            return Response(response, status=status.HTTP_200_OK)
        else:
            # To display direct errors i have created a file named handle_error in utils to display all serialization error
            response = handle_errors(serializer.errors)
            response['result'] = 0
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
 
###############  Login API  ###################
        
class LoginAPIView( generics.GenericAPIView):
    serializer_class = LoginSerializers

    def post(self, request, format=None):

        response = {}
        responsedata = []
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
             #For login purpose used django login and authenticate
            
            #To check user exist or not   
            if not User.objects.filter(username=serializer.validated_data['username'],is_active=True).exists():
                response["result"] = 0
                response["errors"] = ["No user found"]
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if 'username' and 'password' in serializer.validated_data:
                user = authenticate(
                        request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            else:
                response["result"] = 0
                response["errors"] = ["Please enter Username and Password"]
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            #To check valid user or not
            if user is not None:
                login(request, user)
                #Token will generated so that user will use this token for authentication and can view data as token authentication is used in other APIS
                token = Token.objects.update_or_create(user=user)
            else:
                response['result'] = 0
                responsedata.append("Incorrect Username or password")
                response['errors'] = responsedata
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            #result =0 for errors and result =1 for sucess,it's used for data binding in frontend
            #also i have added status of each request in api response
            
            response['token'] = str(token[0])
            response['first_name'] = str(user.first_name)
            response['last_name'] = str(user.last_name)
            response['result'] = 1
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = handle_errors(serializer.errors)
            response['result'] = 0
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        
        
# To view all subscriptions on homepage     
        
############# Subscription API #################     
        
class SubscriptionsAPIView( generics.GenericAPIView):
    """
    Get All data from Subscription
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer
    
    #Here authentication_classes and permission_classes are used for authentication purpose(user must be authenticated to view below api response)
    def get(self, request, format=None):

        response = {}
        responsedata = []
        data = Subscription.objects.all()
        serializer = self.serializer_class(data, many=True)
        response['result'] = 1
        response['data'] = serializer.data
        return Response(response, status=status.HTTP_200_OK)
    
    
# Booking of Subscription

class BookSubscriptionPOSTAPIView( generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BookSubscriptionPOSTSerializer

    # Add Subscription

    def post(self, request, format=None):
        '''
        Book Subscription
        '''

        response = {}
        responsedata = []
        request.data._mutable = True
        # Here i have set request.data mutable=True because the querydicts at request.POST and request.GET will be immutable when accessed in a normal request/response cycle.
        
        # Get the user from requested token to save as created_by while booking
        manager_object = Manager.objects.get(
            user=(request.user))
        request.data['created_by'] = manager_object.id

        serializers = self.serializer_class(data=request.data)
        message = 'Successfully Inserted'

        if serializers.is_valid():

            save_data = serializers.save()
            response["result"] = 1
            responsedata.append(message)
            response['data'] = responsedata
            response['id'] = save_data.id  # id of the booking record which will be used in the next step(payment gateway)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = handle_errors(serializers.errors)
            response['result'] = 0
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        

############### Payment Gateway ################

# Razorpay Order creation API

class ManagerCreateOrderPaymentApiView( generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ManagerOrderSerializer

    def post(self, request, format=None):
        '''
        Payment Gateway  POST
        '''
        response = {}
        responsedata = []
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            booking_id = serializers.validated_data['booking_id']
            
            if BookSubscription.objects.filter(id=booking_id).exists():
                booking_obj = BookSubscription.objects.get(
                    id=booking_id)
                value = Decimal(booking_obj.subscription.amount)

                amount = 0
                if value is not None:
                    amount=(int(value*100))

                user_details = None
                if Manager.objects.filter(user=booking_obj.created_by.user).exists():
                    user_details = Manager.objects.get(
                        user=booking_obj.created_by.user)
                    
                key_id= 'rzp_test_ki1Q8H5SQeqOja'
                key_secret= 'MsIaQgv0RURBRI3biKLnht7S'
                
                # Create razorpay client  
                client= razorpay.Client(auth=(key_id,key_secret))
                
                # create order
                result_of_order=client.order.create(dict(amount=amount,currency='INR'))
                
                order_id=result_of_order['id']
                
                order_status=result_of_order['status']
                
                if order_status == 'created':
                    booking_obj.order_id = order_id
                    booking_obj.save()
                
                response['result'] = 1
                responsedata.append(result_of_order['id'])
                # this order_id will be used in frontend for next process
                response['data'] = responsedata
                return Response(response, status=status.HTTP_200_OK)
            else:
                response['result'] = 0
                responsedata.append("NO SUCH BOOKING FOUND")
                response['data'] = responsedata
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = handle_errors(serializers.errors)
            response["result"] = 0
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        

# Below Api will used after all check out operation done in frontend, 
# then this will receive two params to store in our database and send a sucess or failure msg in response

# I have not done the frontend checkout part,so the below api cann't be tested it's just for view purpose to know the process.

      
class ManagerTransactionCheck( generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ManagerTransactionSerializer

    def post(self, request, format=None):
        '''
        Transaction success  POST
        '''
        response = {}
        responsedata = []
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            order_id = serializers.validated_data['razorpay_order_id']
            p_id = serializers.validated_data['razorpay_payment_id']
            # These two above value will come to backend after after all checkout operation is done in the frontend
            #Will store this values for future(other transaction process) process.
            
            message = ""
            if BookSubscription.objects.get(order_id=order_id).exists():
                booking_obj = BookSubscription.objects.get(order_id=order_id)
                booking_obj.payment_status = "S"
                booking_obj.status = "Active"
                booking_obj.razorpay_payment_id = p_id
                booking_obj.save()
                
                message = "Your Payment Has Been Successful! Your Booking is processed. Thank You!"
            else:
                booking_obj = BookSubscription.objects.get(order_id=order_id)
                booking_obj.payment_status = "F"
                booking_obj.status = "Cancel"
                booking_obj.save()
               
                message = "Sorry your payment has failed,booking is not processed."
            response['result'] = 1
            responsedata.append(message)
            response['data'] = responsedata
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = handle_errors(serializers.errors)
            response["result"] = 0
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        

# To cancel or Resume a subscription

class ManagerSubscriptionStatusAPIView( generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionStatusSerializer

    def post(self, request, format=None):
        '''
        Subscription Resume/Cancel  
        '''
        response = {}
        responsedata = []
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            status_obj = serializers.validated_data['status']
            booking_id = serializers.validated_data['booking_id']
            
            # To check for booking record present or not,if present change it's status
            if BookSubscription.objects.filter(id=booking_id).exists():
                if serializers.validated_data['status'] == "Active":
                    booking_obj = BookSubscription.objects.get(id=booking_id)
                    booking_obj.status = status_obj
                    booking_obj.save()
                    
                    message = "Your Subscription is resumed.Enjoy!!!"
                else:
                    booking_obj = BookSubscription.objects.get(id=booking_id)
                    booking_obj.status = status_obj
                    booking_obj.save()
                    
                    message = "Your Subscription is Cancelled.You can resume it anytime."
            else:
                response["result"] = 0
                response["errors"] = ["No Record Found"]
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            response['result'] = 1
            responsedata.append(message)
            response['data'] = responsedata
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = handle_errors(serializers.errors)
            response["result"] = 0
            return Response(response, status=status.HTTP_400_BAD_REQUEST)