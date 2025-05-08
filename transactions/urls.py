from rest_framework.routers import DefaultRouter
from .views import DepositViewSet, WithdrawalViewSet


# views for super user
router = DefaultRouter()
router.register('deposits', DepositViewSet, basename='deposits')
router.register('withdrawals', WithdrawalViewSet, basename='withdrawals')

urlpatterns = router.urls
