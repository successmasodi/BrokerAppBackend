from django.contrib import admin
from .models import Deposit, Withdrawal, Balance

# admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Balance)

# Register your models here.


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "is_verified")
    list_editable = ("is_verified",)
    list_per_page = 10
    list_filter = ("is_verified",)
    search_fields = ("user__username",)

    class Meta:
        model = Deposit
