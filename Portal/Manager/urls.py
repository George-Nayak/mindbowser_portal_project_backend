from django.urls import path, include
from .views import *

auth_urls = [
    
    path('sign_up', SignUpAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('subscription/get', SubscriptionsAPIView.as_view()),
    path('book_subscription/post', BookSubscriptionPOSTAPIView.as_view()),
    path('create_order', ManagerCreateOrderPaymentApiView.as_view()),
    path('subscription_status_change', ManagerSubscriptionStatusAPIView.as_view()),
]

urlpatterns = [
    path('', include(auth_urls)),
]
