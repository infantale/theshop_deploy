from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from core.models import Bb, AdvUser
from .serializers import *


@api_view(['GET'])
def bbs(request):
    if request.method == 'GET':
        bbs = Bb.objects.filter(is_active=True)[:10]
        serializer = BbSerializer(bbs, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_outfits(request):
    if request.method == 'GET':
        outfits = Outfit.objects.all()
        serializer = OutfitSerializer(outfits, many=True)
        current_user = request.user.id
        data = serializer.data
        data.append({'current_user': current_user})
        return Response(data)


def page_outfits(request):
    return render(request, 'main/outfits.html')


class BbDetailView(RetrieveAPIView):
    queryset = Bb.objects.filter(is_active=True)
    serializer_class = BbDetailSerializer


class PostLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Outfit, pk=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
            likesCount = obj.likes.count()
        data = {'updated': updated, 'liked': liked, 'counter': likesCount}
        return Response(data)

# http://localhost:8000/api/outfits_page/ убрать отсюда количество лайков.
# Отображать только лайк текущего пользователя (Вы уже оценили этот образ)
# Общее количество лайков выводить только в профиле владельца образа

# class UserOutfitsRelationView(UpdateModelMixin, GenericViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = UserOutfitRelation.objects.all()
#     serializer_class = UserOutfitRelationSerializer
#     lookup_field = 'outfit'
#
#     def get_object(self):
#         # print('\n\n\n\n')
#         # print(self.kwargs)
#         # print(self.kwargs['outfit'])
#         # print(type(int(self.kwargs['outfit'])))
#         # print('\n\n\n\n')
#
#         # Если нет связи между пользователем чья сессия на данный момент активна,
#         # и аутфитом в бд,
#         # (модель UserOutfitRelation)
#         # то это не будет работать
#
#         obj, _ = UserOutfitRelation.objects.get_or_create(user=self.request.user, \
#                                     outfit_id=self.kwargs['outfit'])
#         # print(obj)
#         return obj
