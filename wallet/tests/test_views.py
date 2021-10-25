from .test_setup import TestSetUp
from wallet.models import Wallet, Transactions


class TestAccountViews(TestSetUp):
    """Test View for Accounts"""
    def test_get_all_accounts_with_no_data(self):
        """
        With no data in db, entire account summary should be a empty list
        """
        res = self.client.get(self.accounts_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

    def test_get_account_by_id_no_data(self):
        """
        With no data in db, account summary fetch by account_id url param will return a empty list
        """
        res = self.client.get(self.account_by_id_25_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

    def test_get_all_accounts(self):
        """
        Inserted 2 accounts in db, and so returned all account summary length is 2
        """
        self.setup_account_wallet()
        res = self.client.get(self.accounts_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)

    def test_get_account_by_id(self):
        """
        Inserted two accounts with id - 21 & 22, and fetching account by 21 would give you a single result
        """
        self.setup_account_wallet()
        res = self.client.get(self.account_by_id_21_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)


class TestTransactionsView(TestSetUp):
    """
    Test view for get and post transactions
    """
    def test_get_transactions_with_no_data_invalid_wallet_id(self):
        """
        With invlid wallet id, transactions get would return an empty list
        """
        res = self.client.get(self.transactions_wallet_25_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

    def test_get_transactions_for_wallet(self):
        """
        since there is only one transaction in db for wallet_id 21, fetch transactions would return single result
        """
        self.setup_account_wallet()
        res = self.client.get(self.transactions_wallet_21_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)

    def test_payment_transfer_invalid_wallet_id(self):
        """
        If wallet id from where money needs to be debited is invalid / could not be found in db, post transactions would
        throw 404 exception
        """
        self.setup_account_wallet()
        res = self.client.post(self.transactions_wallet_25_url, data={"amount": 100, "referenced_wallet_id": 22},
                               format='json')
        self.assertEqual(res.status_code, 404)

    def test_payment_transfer_invalid_ref_wallet_id(self):
        """
        If referenced wallet id to where money needs to be credited is invalid / could not be found in db,
        post transactions would throw 404 exception
        """
        self.setup_account_wallet()
        res = self.client.post(self.transactions_wallet_21_url, data={"amount": 100, "referenced_wallet_id": 25},
                               format='json')
        self.assertEqual(res.status_code, 404)

    def test_payment_transfer_zero_amount(self):
        """
        If the amount needs to be transferred is zero or less than zero, api call would return 400 Bad request
        """
        self.setup_account_wallet()
        res = self.client.post(self.transactions_wallet_21_url, data={"amount": 0, "referenced_wallet_id": 22},
                               format='json')
        self.assertEqual(res.status_code, 400)

    def test_payment_transfer_negative_amount(self):
        """
        If the amount needs to be transferred is zero or less than zero, api call would return 400 Bad request
        """
        self.setup_account_wallet()
        res = self.client.post(self.transactions_wallet_21_url, data={"amount": -20, "referenced_wallet_id": 22},
                               format='json')
        self.assertEqual(res.status_code, 400)

    def test_payment_transfer_negative_balance(self):
        """
        If the customer wallet balance would become negative after transferring amount, api will throw 422 error
        and will not process transaction

        """
        self.setup_account_wallet()
        res = self.client.post(self.transactions_wallet_21_url, data={"amount": 500, "referenced_wallet_id": 22},
                               format='json')
        self.assertEqual(res.status_code, 422)

    def test_payment_transfer_success_flow(self):
        """
        Success case for payment transfer, the amount debited & credited in respective wallets,
        transaction entries are also made
        """
        self.setup_account_wallet()
        res = self.client.post(self.transactions_wallet_21_url, data={"amount": 10, "referenced_wallet_id": 22},
                               format='json')
        self.assertEqual(res.status_code, 200)
        sender_wallet_obj = Wallet.objects.filter(wallet_id=21)
        recvr_wallet_obj = Wallet.objects.filter(wallet_id=22)
        transaction_objs = Transactions.objects.all()

        self.assertEqual(sender_wallet_obj[0].balance, 290)
        self.assertEqual(recvr_wallet_obj[0].balance, 310)
        self.assertEqual(len(transaction_objs), 4)
