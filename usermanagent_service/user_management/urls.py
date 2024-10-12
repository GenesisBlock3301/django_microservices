from django.urls import path
from .views import *

urlpatterns = [
	path('create/', UserCreateAPIView.as_view(), name='create'),
	path('login/', LoginAPIView.as_view(), name='login'),
]
