from rest_framework import serializers
from transactions.models import Balance, Deposit, Withdrawal

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['id', 'user', 'amount']
        read_only_fields = ['id', 'user', 'amount']  # Make all fields read-only

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'user', 'amount', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'user']

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['id', 'user', 'amount', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'user']

    def validate(self, data):
        return data
