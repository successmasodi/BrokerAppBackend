from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from transactions.models import Deposit, Withdrawal, Balance
from .serializers import DepositSerializer, WithdrawalSerializer, BalanceSerializer
from .filters import DepositFilter, WithdrawalFilter
from decimal import Decimal
from django.core.exceptions import ValidationError

class DepositViewSet(viewsets.ModelViewSet):
    serializer_class = DepositSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DepositFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        deposit = serializer.save(user=self.request.user)
        balance, created = Balance.objects.get_or_create(user=deposit.user)
        balance.amount += Decimal(deposit.amount)
        balance.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        old_amount = instance.amount
        new_instance = serializer.save(user=self.request.user)
        balance, created = Balance.objects.get_or_create(user=new_instance.user)
        new_balance = balance.amount + new_instance.amount - old_amount
        if new_balance < 0:
            serializer._errors['amount'] = ['Insufficient balance after update.']
            return Response(serializer.errors, status=400)
        balance.amount = new_balance
        balance.save()

    def perform_destroy(self, instance):
        balance, created = Balance.objects.get_or_create(user=instance.user)
        balance.amount -= Decimal(instance.amount)
        balance.save()
        instance.delete()

class WithdrawalViewSet(viewsets.ModelViewSet):
    serializer_class = WithdrawalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WithdrawalFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Withdrawal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data['amount']
        try:
            balance = Balance.objects.get(user=user)
            if amount > balance.amount:
                serializer._errors['amount'] = ['Insufficient balance for this withdrawal.']
                return Response(serializer.errors, status=400)
        except Balance.DoesNotExist:
            serializer._errors['amount'] = ['Insufficient balance for this withdrawal.']
            return Response(serializer.errors, status=400)

        withdrawal = serializer.save(user=user)
        balance.amount -= Decimal(withdrawal.amount)
        balance.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        old_amount = instance.amount
        new_instance = serializer.save(user=self.request.user)
        balance, created = Balance.objects.get_or_create(user=new_instance.user)
        new_balance = balance.amount - new_instance.amount + old_amount
        if new_balance < 0:
            serializer._errors['amount'] = ['Insufficient balance after update.']
            return Response(serializer.errors, status=400)
        balance.amount = new_balance
        balance.save()

    def perform_destroy(self, instance):
        balance, created = Balance.objects.get_or_create(user=instance.user)
        balance.amount += Decimal(instance.amount)
        balance.save()
        instance.delete()

class BalanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Balance.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if (queryset.exists()):
            serializer = self.get_serializer(queryset.first())
            return Response(serializer.data)
        else:
            return Response({"id": None, "user": request.user.id, "amount": 0})
