import base64
from datetime import date
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TeamSerializers
from .serializers import TeamInputSerializers
from .serializers import MemberSerializers
from .serializers import UserSerializers
from .models import Member, Team, User
from rest_framework import status
from django.http import Http404
import numpy as np


class Team_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        team = Team.objects.all()
        serializer = TeamSerializers(team, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        imageb64 = None
        if request.data['image']:
            imageb64 = base64.b64encode(request.data['image'].read())
        members = list(request.data['members'].replace('[', '').replace(']', '').replace(',', ''))
        data = {'name': request.data['name'], 'image': imageb64}
        serializerInput = TeamInputSerializers(data=data)
        if serializerInput.is_valid():
            team = serializerInput.save()
            for member in members:
                serializerMember = MemberSerializers(
                    data={'team': team.id, 'user': member, 'date_joined': date.today()})
                if serializerMember.is_valid():
                    serializerMember.save()
            Team.objects.get(pk=team.id)
            serializer = TeamSerializers(team)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Team_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        team = self.get_object(pk)
        serializer = TeamSerializers(team)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        team = self.get_object(pk)
        serializer = TeamSerializers(team)

        imageb64 = None
        if request.data['image']:
            imageb64 = base64.b64encode(request.data['image'].read())
        membersUpdate = list(
            request.data['members'].replace('[', '').replace(']', '').replace(',', ''))
        membersUpdate = list(map(lambda member: int(member), membersUpdate))
        data = {'name': request.data['name'], 'image': imageb64}

        membersDB = list(
            map(lambda member: member['id'], serializer.data['members']))
        serializerInput = TeamInputSerializers(team, data=data)

        if serializerInput.is_valid():
            serializerInput.save()
            if not np.array_equal(membersDB, membersUpdate):
                for memberUpdate in membersUpdate:
                    if not memberUpdate in membersDB:
                        serializerMember = MemberSerializers(
                            data={'team': team.id, 'user': memberUpdate, 'date_joined': date.today()})
                        if serializerMember.is_valid():
                            serializerMember.save()
                for memberDB in membersDB:
                    if not memberDB in membersUpdate:
                        memberGet = Member.objects.get(
                            team=team.id, user=memberDB)
                        memberGet.delete()

            Team.objects.get(pk=team.id)
            serializer = TeamSerializers(team)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        team = self.get_object(pk)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class User_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        user = User.objects.all()
        serializer = UserSerializers(user, many=True)

        return Response(serializer.data)
