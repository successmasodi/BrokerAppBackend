from django.contrib import admin
from .models import Deposit, Withdrawal, Balance

admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Balance)

# Register your models here.
