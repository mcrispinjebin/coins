import json
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.db import transaction

from .models import Transactions, Wallet
from .serializers import WalletSerializer, TransactionSummarySerializer, TransactionPayloadSerializer


# Create your views here.

class AccountsView(APIView):
    """
    View class for account specific operation
    """
    def get(self, request, account_id=None):
        """
        Get Accounts or get Account by account_id
        @param request: api request
        @param account_id: int
        The method returns all accounts if account_id is None or not provided,
        else returns the account for the same account_id.
        """
        print("Incoming Request - ", request)
        if account_id:
            account_id = int(account_id)
            list_accounts = Wallet.objects.filter(account=account_id).select_related("account")
            serializer = WalletSerializer(list_accounts, many=True)
        else:
            list_accounts = Wallet.objects.all().select_related("account")
            serializer = WalletSerializer(list_accounts, many=True)

        return Response(serializer.data)


class TransactionsView(GenericAPIView):
    """
    View class for transaction related operations
    """
    serializer_class = TransactionPayloadSerializer

    def get(self, request, wallet_id):
        """
        Get transactions for wallet_id
        @param request: api request
        @param wallet_id: int - required
        The method returns all transactions related to the specific wallet for customer
        """
        print("Incoming Request - ", request)
        wallet_id = int(wallet_id)

        wallet_transactions = Transactions.objects.filter(wallet_id=wallet_id).select_related("wallet_id").\
            select_related("wallet_id__account")

        serializer = TransactionSummarySerializer(wallet_transactions, many=True)
        return Response(serializer.data)

    def post(self, request, wallet_id):
        """
        Transfer money between wallets
        @param request: api request
        @param wallet_id: int - required
        @body amount: float - required
        @body referenced_wallet_id - required (recipient_wallet_id)
        The method transfers money from wallet_id to referenced_wallet_id, if operation could not be performed,
        4xx error is returned
        """
        try:
            request_body = request.body
            request_dict = json.loads(request_body)
            if not request_dict.get("referenced_wallet_id") or not request_dict.get("amount") or \
                    request_dict["amount"] <= 0:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            amount = request_dict["amount"]

            with transaction.atomic():
                sender_obj = Wallet.objects.select_for_update().get(wallet_id=wallet_id)
                if sender_obj.balance - amount <= 0:
                    return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                receiver_obj = Wallet.objects.select_for_update().get(wallet_id=request_dict["referenced_wallet_id"])

                payout_tran = Transactions(wallet_id=sender_obj, amount=amount,
                                           transaction_type="payout", status="success",
                                           referenced_wallet_id=receiver_obj, created_at=datetime.now(),
                                           created_by="payment_module")

                payin_tran = Transactions(wallet_id=receiver_obj, amount=amount,
                                          transaction_type="payin", status="success",
                                          referenced_wallet_id=sender_obj, created_at=datetime.now(),
                                          created_by="payment_module")

                sender_obj.balance = sender_obj.balance - amount
                receiver_obj.balance = receiver_obj.balance + amount

                payout_tran.save()
                payin_tran.save()
                sender_obj.save()
                receiver_obj.save()
        except ObjectDoesNotExist as e:
            print("Exception raised -", str(e))
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)
