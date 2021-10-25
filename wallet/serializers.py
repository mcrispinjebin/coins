from rest_framework import serializers
from .models import Account, Transactions, Wallet


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Wallet
        fields = ["account", "wallet_type", "balance", "currency_type"]


class AccountSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["account_id", "first_name"]


class WalletSummarySerializer(serializers.ModelSerializer):
    account = AccountSummarySerializer()

    class Meta:
        model = Wallet
        fields = ["account"]


class TransactionSummarySerializer(serializers.ModelSerializer):
    referenced_wallet_id = WalletSummarySerializer()

    class Meta:
        model = Transactions
        fields = ["transaction_id", "transaction_type", "amount", "referenced_wallet_id", "created_at"]


class TransactionPayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ["amount", "referenced_wallet_id"]
