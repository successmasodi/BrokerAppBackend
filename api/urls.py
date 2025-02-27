from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepositViewSet, WithdrawalViewSet, BalanceViewSet

router = DefaultRouter()
router.register('deposits', DepositViewSet, basename='deposits')
router.register('withdrawals', WithdrawalViewSet, basename='withdrawals')
router.register('balance', BalanceViewSet, basename='balance')

urlpatterns = [
    path('', include(router.urls)),
]
