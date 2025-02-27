import django_filters
from transactions.models import Deposit, Withdrawal

class DepositFilter(django_filters.FilterSet):
    day = django_filters.NumberFilter(field_name='timestamp__day', label='Day')
    month = django_filters.NumberFilter(field_name='timestamp__month', label='Month')
    year = django_filters.NumberFilter(field_name='timestamp__year', label='Year')

    class Meta:
        model = Deposit
        fields = ['day', 'month', 'year']

class WithdrawalFilter(django_filters.FilterSet):
    day = django_filters.NumberFilter(field_name='timestamp__day', label='Day')
    month = django_filters.NumberFilter(field_name='timestamp__month', label='Month')
    year = django_filters.NumberFilter(field_name='timestamp__year', label='Year')

    class Meta:
        model = Withdrawal
        fields = ['day', 'month', 'year']
