from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('v1/team', Team_APIView.as_view()),
    path('v1/team/<int:pk>/', Team_APIView_Detail.as_view()),
    path('v1/user', User_APIView.as_view()),
]
