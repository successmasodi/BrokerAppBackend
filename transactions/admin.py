from django.contrib import admin
from .models import Deposit, Withdrawal, Balance, AccountSummary

admin.site.register(Balance)

# Register your models here.


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "is_verified")
    list_editable = ("is_verified",)
    list_per_page = 10
    list_filter = ("is_verified",)
    search_fields = ("user__username",)
    ordering = ('timestamp', 'is_verified')

    class Meta:
        model = Deposit


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "is_verified")
    list_editable = ("is_verified",)
    list_per_page = 10
    list_filter = ("is_verified",)
    search_fields = ("user__username",)
    ordering = ('timestamp', 'is_verified')

    class Meta:
        model = Withdrawal


@admin.register(AccountSummary)
class AccountSummaryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "profit_loss", "margin",
                    "free_margin", "margin_level", "opened_position")
    list_editable = ("profit_loss", "margin", "free_margin",
                     "margin_level", "opened_position")
    list_per_page = 10
    search_fields = ("user__username",)
    ordering = ("opened_position", "-free_margin")

    class Meta:
        model = AccountSummary
