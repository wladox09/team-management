from django.urls import path

from api.tasks import check_size_team

from .views import *

app_name = 'api'

check_size_team(repeat=300)

urlpatterns = [
    path('v1/team', Team_APIView.as_view()),
    path('v1/team/<int:pk>/', Team_APIView_Detail.as_view()),
    path('v1/user', User_APIView.as_view()),
]