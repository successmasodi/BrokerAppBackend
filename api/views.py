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
        print("Performing create for deposit")
        try:
            deposit = serializer.save(user=self.request.user)
            print(f"Deposit created: {deposit}")
            balance, created = Balance.objects.get_or_create(user=deposit.user)
            print(f"Balance retrieved/created: {balance}, created: {created}")
            balance.amount += Decimal(deposit.amount)
            balance.save()
            print(f"Balance updated: {balance.amount}")
        except serializers.ValidationError as e:
            print(f"Validation errors: {e.detail}")
            return Response(e.detail, status=400)

    def perform_update(self, serializer):
        print("Performing update for deposit")
        try:
            instance = self.get_object()
            old_amount = instance.amount
            new_instance = serializer.save(user=self.request.user)
            print(f"Deposit updated: {new_instance}")
            balance, created = Balance.objects.get_or_create(user=new_instance.user)
            print(f"Balance retrieved/created: {balance}, created: {created}")
            new_balance = balance.amount + Decimal(new_instance.amount) - Decimal(old_amount)
            balance.amount = new_balance
            balance.save()
            print(f"Balance updated: {balance.amount}")
        except serializers.ValidationError as e:
            print(f"Validation errors: {e.detail}")
            return Response(e.detail, status=400)

    def perform_destroy(self, instance):
        print("Performing destroy for deposit")
        balance, created = Balance.objects.get_or_create(user=instance.user)
        print(f"Balance retrieved/created: {balance}, created: {created}")
        balance.amount -= Decimal(instance.amount)
        balance.save()
        print(f"Balance updated: {balance.amount}")
        instance.delete()
        print("Deposit deleted")

class WithdrawalViewSet(viewsets.ModelViewSet):
    serializer_class = WithdrawalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WithdrawalFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Withdrawal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        print("Performing create for withdrawal")
        try:
            withdrawal = serializer.save(user=self.request.user)
            print(f"Withdrawal created: {withdrawal}")
            balance = Balance.objects.get(user=withdrawal.user)
            balance.amount -= Decimal(withdrawal.amount)
            balance.save()
            print(f"Balance updated: {balance.amount}")
        except serializers.ValidationError as e:
            print(f"Validation errors: {e.detail}")
            return Response(e.detail, status=400)

    def perform_update(self, serializer):
        print("Performing update for withdrawal")
        try:
            instance = self.get_object()
            old_amount = instance.amount
            new_instance = serializer.save(user=self.request.user)
            print(f"Withdrawal updated: {new_instance}")
            balance, created = Balance.objects.get_or_create(user=new_instance.user)
            print(f"Balance retrieved/created: {balance}, created: {created}")
            new_balance = balance.amount - Decimal(new_instance.amount) + Decimal(old_amount)
            balance.amount = new_balance
            balance.save()
            print(f"Balance updated: {balance.amount}")
        except serializers.ValidationError as e:
            print(f"Validation errors: {e.detail}")
            return Response(e.detail, status=400)

    def perform_destroy(self, instance):
        print("Performing destroy for withdrawal")
        balance, created = Balance.objects.get_or_create(user=instance.user)
        print(f"Balance retrieved/created: {balance}, created: {created}")
        balance.amount += Decimal(instance.amount)
        balance.save()
        print(f"Balance updated: {balance.amount}")
        instance.delete()
        print("Withdrawal deleted")

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
