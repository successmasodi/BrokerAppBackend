from rest_framework import serializers
from transactions.models import Balance, Deposit, Withdrawal
from decimal import Decimal

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['id', 'user', 'amount']
        read_only_fields = ['id', 'user', 'amount']


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'user', 'amount', 'is_verified','timestamp']
        read_only_fields = ['id', 'timestamp', 'user', 'is_verified']

    def validate(self, data):
        " Validate that ordinary users cannot update verified deposits and amount is greater than 0."

        user = self.context['request'].user
        balance, created = Balance.objects.get_or_create(user=user)
        if Decimal(balance.amount) + Decimal(data['amount']) < 0:
            raise serializers.ValidationError({'error': 'Insufficient balance after deposit.'})

        instance = self.instance
        if instance and instance.is_verified and not user.is_staff:
            raise serializers.ValidationError("You can't update an already verified deposit.")

        return data


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['id', 'user', 'amount', 'is_verified' , 'timestamp']
        read_only_fields = ['id', 'timestamp', 'user', 'is_verified']

    def validate(self, data):
        user = self.context['request'].user
        try:
            balance = Balance.objects.get(user=user)
            if Decimal(data['amount']) > Decimal(balance.amount):
                raise serializers.ValidationError({'error': 'Insufficient balance for this withdrawal.'})
        except Balance.DoesNotExist:
            raise serializers.ValidationError({'error': 'Insufficient balance for this withdrawal.'})
        return data
