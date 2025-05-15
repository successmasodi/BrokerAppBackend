from rest_framework import serializers
from .models import Deposit, Withdrawal, Balance, AccountSummary


class BaseUserdataSerializer(serializers.ModelSerializer):
    ''' inherit user data from here to be more readable '''
    user_data = serializers.SerializerMethodField()

    def get_user_data(self, obj):
        return {
            "id": obj.user.id,
            "user_email": obj.user.email
        }


class ManagerDepositSerializer(BaseUserdataSerializer):

    class Meta:
        model = Deposit
        fields = ['id', 'user_data', 'amount', 'is_verified', 'timestamp']
        read_only_fields = ('id', 'user_data')


class ManagerWithdrawalSerializer(BaseUserdataSerializer):

    class Meta:
        model = Withdrawal
        fields = ['id', 'user_data', 'amount', 'is_verified', 'timestamp']
        read_only_fields = ('id', 'user_data')


class ManageBalanceSerializer(BaseUserdataSerializer):

    class Meta:
        model = Balance
        fields = ('id', 'user_data', 'amount')
        read_only_fields = ('id', 'user_data')


class ManageAccountSummarySerializer(BaseUserdataSerializer):

    class Meta:
        model = AccountSummary
        fields = ['id', 'user_data', 'profit_loss', 'opened_position',
                  'margin', 'free_margin', 'margin_level']
        read_only_fields = ('id', 'user_data')
