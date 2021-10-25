from datetime import datetime
from rest_framework.test import APITestCase
from django.urls import reverse
from wallet.models import Account, Wallet, Transactions


class TestSetUp(APITestCase):
    def setUp(self):
        self.accounts_url = reverse("all_accounts")
        self.account_by_id_25_url = reverse("single_account", args=[25])
        self.account_by_id_21_url = reverse("single_account", args=[21])
        self.transactions_wallet_25_url = reverse("transaction_summary", args=[25])
        self.transactions_wallet_21_url = reverse("transaction_summary", args=[21])

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def setup_account_wallet(self, transaction_amount=100):
        self.first_account = Account.objects.create(account_id=21, first_name="crispin", last_name="m", gender="m",
                                                    date_of_birth="1994-11-11", title="mr",
                                                    email="crispinjebin@gmail.com", status="active",
                                                    created_at="2021-10-24", updated_at=None, updated_by=None)

        self.first_wallet = Wallet.objects.create(wallet_id=21, account=self.first_account, wallet_type="premium",
                                                  balance="300", currency_type="usd")

        self.second_account = Account.objects.create(account_id=22, first_name="srini", last_name="s", gender="m",
                                                     date_of_birth="1994-12-12", title="mr",
                                                     email="srini.s@gmail.com", status="active",
                                                     created_at="2021-10-24", updated_at=None, updated_by=None)

        self.second_wallet = Wallet.objects.create(wallet_id=22, account=self.second_account, wallet_type="premium",
                                                   balance="300", currency_type="usd")

        self.first_transaction = Transactions.objects.create(wallet_id=self.first_wallet, amount=transaction_amount,
                                                             transaction_type="payout", status="success",
                                                             referenced_wallet_id=self.second_wallet,
                                                             created_at=datetime.now(), created_by="payment_module")

        self.second_transaction = Transactions.objects.create(wallet_id=self.second_wallet, amount=transaction_amount,
                                                              transaction_type="payout", status="success",
                                                              referenced_wallet_id=self.first_wallet,
                                                              created_at=datetime.now(), created_by="payment_module")
