from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from decimal import Decimal

from decimal import  Decimal

class Balance(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"


class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-timestamp","is_verified")

    def __str__(self):
        return f"{self.user.username} - Deposit - {self.amount}"

    def save(self, *args, **kwargs):
        """increase the balance if deposit is just verified and vice versa"""
        print("calling the save method of Deposit")
        try:
            # forcing to make sure the status is false when a deposit is just created
            if not self.pk:
                self.is_verified = False
            else:
                old_deposit = Deposit.objects.get(pk=self.pk)
                old_verified = old_deposit.is_verified
                old_amount = Decimal(old_deposit.amount)

                instance_verified = self.is_verified
                instance_amount = Decimal(self.amount)

                value = Decimal(0)

                if old_verified and not instance_verified:
                    # we want to subtract from balance because we have added it when it was first verified
                    value -= old_amount
                    print(f'i am working on 1 block value:{value}')
                if instance_verified and not old_verified:
                    value += instance_amount
                    print(f'i am working on 2 block value:{value}')
                if instance_verified and old_verified:
                    value += instance_amount - old_amount
                    print(f'i am working on 3 block value:{value}')

                balance, created = Balance.objects.get_or_create(
                    user=old_deposit.user)
                print(
                    f'updating balance with {value}, new amount:{instance_amount}, old amount : {old_amount}, Balance: {balance} ')
                if value != 0:
                    balance.amount += value
                    balance.save()

            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"An error occurred while saving the deposit:{str(e)}")

    def save(self, *args, **kwargs):
        """increase the balance if deposit is just verified and vice versa"""
        try:
            if self.pk:
                old_deposit = Deposit.objects.get(pk=self.pk)
                old_verified = old_deposit.is_verified
                old_amount = Decimal(old_deposit.amount)

                new_verified = self.is_verified
                new_amount = Decimal(self.amount)

                value = Decimal(0)

                if old_verified and not new_verified:
                    # we want to subtract from balance because we have added it when it was first verified
                    value -= old_amount
                    print(f'i am working on 1 block value:{value}')
                if new_verified and not old_verified:
                    value += new_amount
                    print(f'i am working on 2 block value:{value}')
                if new_verified and old_verified:
                    value += new_amount - old_amount
                    print(f'i am working on 3 block value:{value}')

                balance, created = Balance.objects.get_or_create(user=old_deposit.user)
                print(f'updating balance with {value}, new amount:{new_amount}, old amount : {old_amount}, Balance: {balance} ')
                if value != 0:
                    balance.amount += value
                    balance.save()

            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"An error occurred: {str(e)}")


class Withdrawal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-timestamp", "is_verified")

    def __str__(self):
        return f"{self.user.username} - Withdrawal - {self.amount}"

    def clean(self):
        balance = Balance.objects.get(user=self.user)
        if self.amount > balance.amount:
            raise ValidationError('Insufficient balance for this withdrawal.')

    def save(self, *args, **kwargs):
        """
        balance should be deducted when a staff verify a withdrawal.
        balance should increase when a staff unverify a withdrawal
        """
        print("calling the save method of withdrawal")
        self.clean()
    
        try:
            # Ensure that a newly created withdrawal is not marked as verified
            if not self.pk:
                self.is_verified = False
            else:
                old_withdrawal = Withdrawal.objects.get(pk=self.pk)
                balance = Balance.objects.get(user=old_withdrawal.user)

                # a withdrawal status changes to verify, deduct balance
                if self.is_verified and not old_withdrawal.is_verified:
                    balance.amount -= Decimal(self.amount)
                    balance.save()
                    print(
                        f"Balance deducted after withdrawal is verify: {balance.amount}")

                # a withdrawal status changes to unverify, increase balance
                elif not self.is_verified and old_withdrawal.is_verified:
                    balance.amount += Decimal(self.amount)
                    balance.save()
                    print(
                        f"Balance increased after withdrawal is unverify: {balance.amount}")
                
                # adjust the balance when the withdrawal amount changes.
                elif self.is_verified and old_withdrawal.is_verified:
                    balance.amount -= Decimal(self.amount) - Decimal(old_withdrawal.amount) 
                    balance.save()
                    print(
                        f"Balance increased after withdrawal is unverify: {balance.amount}")

            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"An error occurred while saving the withdrawal: {e}")


class Position(models.Model):

    POSITION_TYPES = (("LONG", "Long"), ("SHORT", "Short"))
    STATUS_CHOICES = (("OPEN", "Open"), ("CLOSED", "Closed"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)  # e.g., BTC/USD
    position_type = models.CharField(max_length=5, choices=POSITION_TYPES)
    entry_price = models.DecimalField(max_digits=20, decimal_places=8,null=True, blank=True)
    exit_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    lot_size = models.DecimalField(max_digits=20, decimal_places=8)  # Position size in base currency
    leverage = models.IntegerField(default=1)  # Leverage used (e.g., 10x)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default="OPEN")
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Open Position for {self.user.username} on {self.symbol}"
