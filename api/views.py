from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from transactions.models import Deposit, Withdrawal, Balance
from .serializers import DepositSerializer, WithdrawalSerializer, BalanceSerializer
from .filters import DepositFilter, WithdrawalFilter
from decimal import Decimal
from .permissions import IsOwnerOrReadOnly

class DepositViewSet(viewsets.ModelViewSet):
    serializer_class = DepositSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DepositFilter
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Deposit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        print("Performing create for deposit")
        try:
            deposit = serializer.save(user=self.request.user)
            print(f"Deposit created: {deposit}")

        except serializers.ValidationError as e:
            print(f"Validation errors: {e.detail}")
            return Response(e.detail, status=400)

    def perform_update(self, serializer):
        print("Performing update for deposit")
        try:
            instance = self.get_object()
            old_amount = Decimal(instance.amount)
            old_verified = instance.is_verified

            # if the deposit that is to be updated is already verified, Not allowed
            print(f"PREVIOUS DEPOSIT STATUS {old_verified} ")
             # If the deposit is already verified, raise an error
            if old_verified:
                raise serializers.ValidationError("You can't update an already verified deposit.")

            new_instance = serializer.save(user=self.request.user)
            print(f"Deposit updated: {new_instance} , Verified: {new_instance.is_verified}")

            new_amount = Decimal(new_instance.amount)
            new_verified = new_instance.is_verified

            value = Decimal(0)
            # a user can only modify unverified deposit
            if not (old_verified and new_verified):
                print(not (old_verified or new_verified))
                value = new_amount - old_amount

            if value != 0:
                balance, created = Balance.objects.get_or_create(user=new_instance.user)
                print(f"Balance retrieved/created: {balance}, created: {created}")
                balance.amount += value
                balance.save()
                print(f"Balance updated: {balance.amount}")
    
        except serializers.ValidationError as e:
            print(f"Validation errors: {e.detail}")
            return Response(e.detail, status=400)


    def destroy(self, request, *args, **kwargs):
        """ 
        Overwrites the default destroy method. We want to make sure only staff can delete 
        a verified post and while use can delete their own unverified deposit
        """
        print("performing Delete for deposit")

        try:
            instance = self.get_object()

            if instance.is_verified and not request.user.is_staff:
                return Response(
                            {"detail": "You can't delete an already verified deposit."},
                            status=status.HTTP_403_FORBIDDEN,
                        )

            balance = Balance.objects.get(user=instance.user)
            balance.amount -= Decimal(instance.amount)
            balance.save()
            print(f"Balance updated by subtracting {instance.amount}. New balance: {balance.amount}, Deleted by: {request.user.is_staff}")

            # Delete the deposit
            instance.delete()
            print("Deposit deleted")

            return Response(
                    {"detail": "Deposit deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT,
                )
        except Exception as e:
            print(f"Deposit not verified: {e}")
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'] , permission_classes=[IsAdminUser])
    def verify(self, request, pk):
        """ Verify the status of a deposit by a staff"""
        try:
            deposit = Deposit.objects.get(id=pk)
            if deposit.is_verified:
                return Response(
                    data={"message": "Deposit is initially verified!"},
                    status=status.HTTP_400_BAD_REQUEST
                    )

            # not verified
            deposit.is_verified = True
            deposit.save()
            print(f"Deposit verified successfully amount {deposit.amount}")

            balance, created = Balance.objects.get_or_create(user=deposit.user)
            balance.amount += Decimal(deposit.amount)
            balance.save()
            print(f"Balance updated successfully new amount {deposit.amount},first time depositing:{created}")

            return Response(
                data={"message": "Deposit verified successfully", "new balance": balance.amount},
                status= status.HTTP_200_OK
            )
        except Exception as e:
            print(f"Deposit not verified: {e}")
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


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
        if self.request.user.is_staff:
            return Balance.objects.all()
        return Balance.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if (queryset.exists()):
            serializer = self.get_serializer(queryset,many=True)
            return Response(serializer.data)
        else:
            return Response({"id": None, "user": request.user.id, "amount": 0})
