from django.db import models


class Account(models.Model):
    class Meta:
        db_table = "account"

    STATUS_CHOICES = [("active", "Active"), ("pending", "Pending"), ("deactivated", "De - Activated")]
    TITLE_CHOICES = [("mr", "Mr"), ("ms", "Miss"), ("mrs", "Mrs"), ("dr", "Dr")]
    GENDER_CHOICES = [("m", "Male"), ("f", "Female"), ("t", "Transgender")]

    account_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    title = models.CharField(max_length=4, choices=TITLE_CHOICES)
    email = models.CharField(max_length=50)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    created_at = models.DateField()
    created_by = models.CharField(max_length=50)
    updated_at = models.DateField(null=True, blank=True, default=None)
    updated_by = models.CharField(max_length=50, null=True, default=None, blank=True)


class Wallet(models.Model):
    class Meta:
        db_table = "wallet"

    WALLET_CHOICES = [("food", "Food Wallet"), ("premium", "Premium Wallet")]
    CURRENCY_CHOICES = [("inr", "Indian Rupees"), ("usd", "US Dollars")]

    wallet_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, models.CASCADE, related_name="linked_account")
    wallet_type = models.CharField(max_length=10, choices=WALLET_CHOICES)
    balance = models.DecimalField(decimal_places=2, max_digits=10)
    currency_type = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="usd")


class Transactions(models.Model):
    class Meta:
        db_table = "transactions"

    STATUS_CHOICES = [("success", "Success"), ("failure", "Failure")]
    TYPES_CHOICES = [("payin", "Payin"), ("payout", "Payout")]

    transaction_id = models.AutoField(primary_key=True)
    wallet_id = models.ForeignKey(Wallet, models.CASCADE, related_name="from_wallet")
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    transaction_type = models.CharField(max_length=10, choices=TYPES_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    referenced_wallet_id = models.ForeignKey(Wallet, models.CASCADE, related_name="to_wallet")
    created_at = models.DateField()
    created_by = models.CharField(max_length=50)
    updated_at = models.DateField(null=True, blank=True, default=None)
    updated_by = models.CharField(max_length=50, null=True, default=None, blank=True)
