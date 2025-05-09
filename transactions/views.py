from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import  ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Deposit, Withdrawal, Balance, AccountSummary
from .serializers import ManagerDepositSerializer, ManagerWithdrawalSerializer, ManageBalanceSerializer, ManageAccountSummarySerializer
from .permissions import IsStaffOnly


class BalanceViewSet(ModelViewSet):
    '''
    only super user can access
    filter by timestamp and is verified,
    search by user username
    '''
    queryset = Balance.objects.select_related('user')
    permission_classes = [IsStaffOnly]
    serializer_class = ManageBalanceSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username']

for method in ['list', 'retrieve', 'create', 'partial_update', 'update', 'destroy']:
    BalanceViewSet = method_decorator(name=method, decorator=swagger_auto_schema(tags=['manage']))(BalanceViewSet)


class DepositViewSet(ModelViewSet):
    '''
    only super user can access
    filter by timestamp and is verified,
    search by user username
    '''
    queryset = Deposit.objects.select_related('user')
    permission_classes = [IsStaffOnly]
    serializer_class = ManagerDepositSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = ['timestamp', 'is_verified']

for method in ['list', 'retrieve', 'create', 'partial_update', 'update', 'destroy']:
    DepositViewSet = method_decorator(name=method, decorator=swagger_auto_schema(tags=['manage']))(DepositViewSet)


class WithdrawalViewSet(ModelViewSet):
    '''
    only super user can access
    filter by timestamp and is verified,
    search by user username
    '''
    queryset = Withdrawal.objects.select_related('user')
    serializer_class = ManagerWithdrawalSerializer
    permission_classes = [IsStaffOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = ['timestamp', 'is_verified']

for method in ['list', 'retrieve', 'create', 'partial_update', 'update', 'destroy']:
    WithdrawalViewSet = method_decorator(name=method, decorator=swagger_auto_schema(tags=['manage']))(WithdrawalViewSet)


class AccountSummaryViewSet(ModelViewSet):
    """
    This views shows the admin the account summary including details like
    profit_loss, opened_position and they can modify the details
    """
    queryset = AccountSummary.objects.select_related('user')
    serializer_class = ManageAccountSummarySerializer
    permission_classes = [IsStaffOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = [ 'opened_position', 'margin', 'opened_position']

for method in ['list', 'retrieve', 'create', 'partial_update', 'update', 'destroy']:
    AccountSummaryViewSet = method_decorator(
        name=method, decorator=swagger_auto_schema(tags=['manage']))(AccountSummaryViewSet)
