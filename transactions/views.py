from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import  ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Deposit, Withdrawal
from .serializers import ManagerDepositSerializer, ManagerWithdrawalSerializer
from .permissions import IsStaffOnly


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
    DepositViewSet = method_decorator(name=method, decorator=swagger_auto_schema(tags=['Manage']))(DepositViewSet)


class WithdrawalViewSet(ModelViewSet):
    '''
    only super user can access
    filter by timestamp and is verified,
    search by user username
    '''
    queryset = Withdrawal.objects.select_related('user')
    permission_classes = [IsStaffOnly]
    serializer_class = ManagerWithdrawalSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = ['timestamp', 'is_verified']
