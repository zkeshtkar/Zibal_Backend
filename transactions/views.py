from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Transaction, CachedTransaction
from transactions.serializers import TransactionSerializer, CachedTransactionSerializer


class TransactionView(APIView):
    serializer_class = TransactionSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        serialized_transactions = self.serializer_class(data=request.data)
        try:
            if serialized_transactions.is_valid():
                type = request.data['type']
                mode = request.data['mode']
                merchant_id = request.data.get('merchantId', None)
                transactions = Transaction.retrieve_all_transactions(mode=mode, type=type, merchant_id=merchant_id)
                serialized_transactions = TransactionSerializer(instance=transactions, many=True,
                                                                context={"mode": mode})
                return Response(status=status.HTTP_200_OK, data=serialized_transactions.data)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized_transactions.errors, status=status.HTTP_400_BAD_REQUEST)


class CachedTransactionView(APIView):
    serialized_cached_transactions = CachedTransactionSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        serialized_cached_transactions = self.serialized_cached_transactions(data=request.data)
        try:
            if serialized_cached_transactions.is_valid():
                type = request.data['type']
                mode = request.data['mode']
                merchant_id = request.data.get('merchantId', None)
                if merchant_id is not None:
                    cached_transactions = CachedTransaction.retrieve_all_cached_transactions(mode=mode, type=type,
                                                                                             merchant_id=merchant_id)
                else:
                    cached_transactions = CachedTransaction.retrieve_all_cached_transactions(mode=mode, type=type)
                serialized_cached_transactions = CachedTransactionSerializer(instance=cached_transactions, many=True,
                                                                             context={"mode": mode})
                return Response(status=status.HTTP_200_OK, data=serialized_cached_transactions.data)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(serialized_cached_transactions.errors, status=status.HTTP_400_BAD_REQUEST)
