from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import  ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Deposit, Withdrawal
from .serializers import ManagerDepositSerializer, ManagerWithdrawalSerializer
from .permissions import IsSuperUser


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Manage']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Manage']))
class DepositViewSet(ReadOnlyModelViewSet):
    '''
    only super user can access
    filter by timestamp and is verified,
    search by user username
    '''
    queryset = Deposit.objects.select_related('user')
    permission_classes = [IsSuperUser]
    serializer_class = ManagerDepositSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = ['timestamp', 'is_verified']


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Manage']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Manage']))
class WithdrawalViewSet(ReadOnlyModelViewSet):
    '''
    only super user can access
    filter by timestamp and is verified,
    search by user username
    '''
    queryset = Withdrawal.objects.select_related('user')
    permission_classes = [IsSuperUser]
    serializer_class = ManagerWithdrawalSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = ['timestamp', 'is_verified']
