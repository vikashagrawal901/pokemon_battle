from django.urls import path
from .views import *

urlpatterns = [
    path('battles/', BattleListView.as_view(), name='battle-list'),
    path('battles/create/', BattleCreateView.as_view(), name='battle-create'),
    path('battles/status/<uuid:battle_id>/', BattleStatusView.as_view(), name='battle-status'),
]
