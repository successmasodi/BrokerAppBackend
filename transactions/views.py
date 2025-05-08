from rest_framework.viewsets import  ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Deposit, Withdrawal
from .serializers import DepositSerializer, WithdrawalSerializer
from .permissions import IsSuperUser


class DepositViewSet(ReadOnlyModelViewSet):
    '''
    only super user can access
    filter by timestamp and is verified,
    search by user username
    '''
    queryset = Deposit.objects.select_related('user')
    permission_classes = [IsSuperUser]
    serializer_class = DepositSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = ['timestamp', 'is_verified']


class WithdrawalViewSet(ReadOnlyModelViewSet):
    '''
    only super user can access
    filter by timestamp and is verified,
    search by user username
    '''
    queryset = Withdrawal.objects.select_related('user')
    permission_classes = [IsSuperUser]
    serializer_class = WithdrawalSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = ['timestamp', 'is_verified']
