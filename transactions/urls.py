from rest_framework.routers import DefaultRouter
from .views import DepositViewSet, WithdrawalViewSet, BalanceViewSet, AccountSummaryViewSet


# views for super user
router = DefaultRouter()
router.register('deposits', DepositViewSet, basename='deposits')
router.register('withdrawals', WithdrawalViewSet, basename='withdrawals')
router.register('balances', BalanceViewSet, basename='balances')
router.register('account-summaries', AccountSummaryViewSet, basename='account_sumaries')

urlpatterns = router.urls
