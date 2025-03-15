from django.contrib import admin
from .models import Deposit, Withdrawal, Balance, AccountSummary, Position

admin.site.register(Balance)

# Register your models here.


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ("id","user", "amount", "is_verified")
    list_editable = ("is_verified",)
    list_per_page = 10
    list_filter = ("is_verified",)
    search_fields = ("user__username",)
    ordering = ('timestamp','is_verified')

    class Meta:
        model = Deposit


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ("id","user", "amount", "is_verified")
    list_editable = ("is_verified",)
    list_per_page = 10
    list_filter = ("is_verified",)
    search_fields = ("user__username",)
    ordering = ('timestamp','is_verified')

    class Meta:
        model = Withdrawal


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "symbol", "position_type","profit_loss" ,"entry_price", "exit_price", "lot_size", "leverage", "status", "created_at")
    list_editable = ("status", "profit_loss")
    list_per_page = 10
    list_filter = ("status", "position_type", "symbol")
    search_fields = ("user__username", "symbol")
    ordering = ("-created_at", "status")

    class Meta:
        model = Position


@admin.register(AccountSummary)
class AccountSummaryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "margin" ,"free_margin", "margin_level")
    list_editable = ("margin", "free_margin" ,"margin_level")
    list_per_page = 10
    search_fields = ("user__username",)
    ordering = ("-free_margin",)

    class Meta:
        model = AccountSummary
