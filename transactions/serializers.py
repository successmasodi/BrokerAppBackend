from rest_framework import serializers
from .models import Deposit, Withdrawal


class ManagerDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'user', 'amount', 'is_verified', 'timestamp']
        read_only_fields = ('id', 'user')


class ManagerWithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['id', 'user', 'amount', 'is_verified', 'timestamp']  
        read_only_fields = ('id', 'user')
