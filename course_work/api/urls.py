from django.urls import path
from rest_framework.routers import SimpleRouter

# from .viewsets import OutfitViewSet
from .views import *

app_name = 'api'
# Создаём Router и регистрируем ViewSet
router = SimpleRouter()
# router.register(r'outfit_relation', UserOutfitsRelationView)

urlpatterns = [
    path('bbs/<int:pk>/', BbDetailView.as_view()),
    path('outfit/<int:pk>/like/', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('outfits_page/', page_outfits, name='page_outfits'),
    path('outfits/', get_outfits, name='get_outfits'),
    path('bbs/', bbs),
]

# urlpatterns += router.urls
