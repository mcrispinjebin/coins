from django.contrib import admin
from .models import Account, Wallet, Transactions
# Register your models here.


admin.site.register(Account)
admin.site.register(Wallet)
admin.site.register(Transactions)
