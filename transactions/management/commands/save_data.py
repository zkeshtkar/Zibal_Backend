import bson.errors
from django.core.management.base import BaseCommand, CommandError

from transactions.models import Transaction, CachedTransaction
from transactions.serializers import TransactionSerializer, CachedTransactionSerializer


class Command(BaseCommand):
    help = "Creates the collections needed to use the mongodb cache backend."

    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument(
            '--type', type=str,
            help='Specifies the type for make query ',
        )
        parser.add_argument(
            '--mode', type=str,
            help='Specifies the mode for make query ',
        )
        parser.add_argument(
            '--merchantId', type=str,
            help='Specifies the merchantId for make query ',
        )

    def handle(self, *app_labels, **options):
        mode = options['mode']
        type = options['type']
        merchant_id = options['merchantId'] or None
        try:
            transactions = Transaction.retrieve_all_transactions(mode=mode, type=type, merchant_id=merchant_id)
            serialized_transactions = TransactionSerializer(instance=transactions, many=True, context={"mode": mode})
            data = serialized_transactions.data
            if merchant_id is not None:
                CachedTransaction.objects.filter(mode=mode, type=type,
                                                 merchant_id=merchant_id).delete()
            else:
                CachedTransaction.objects.filter(mode=mode, type=type).delete()
            for transaction in data:
                serialized_transactions = CachedTransactionSerializer(data=transaction,
                                                                      context={"mode": mode, "type": type,
                                                                               "merchant_id": merchant_id})
                if serialized_transactions.is_valid():
                    serialized_transactions.create(validated_data=serialized_transactions.data)

        except bson.errors.InvalidId:
            raise CommandError("use correct id")
