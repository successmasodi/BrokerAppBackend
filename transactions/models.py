from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from decimal import  Decimal

class Balance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-timestamp","is_verified")

    def __str__(self):
        return f"{self.user.username} - Deposit - {self.amount}"

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Withdrawal - {self.amount}"

    def clean(self):
        balance = Balance.objects.get(user=self.user)
        if self.amount > balance.amount:
            raise ValidationError('Insufficient balance for this withdrawal.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
