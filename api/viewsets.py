# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
#
# from core.models import Outfit
# from likes.api.mixins import LikedMixin
# from .serializers import OutfitSerializer
#
#
# class OutfitViewSet(LikedMixin, viewsets.ModelViewSet):
#     queryset = Outfit.objects.all()
#     serializer_class = OutfitSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
