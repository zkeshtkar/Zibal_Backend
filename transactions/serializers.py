import calendar

from transactions.models import CachedTransaction, Transaction
from rest_framework_mongoengine.serializers import DocumentSerializer


class TransactionSerializer(DocumentSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def to_representation(self, instance):
        key = instance['key']
        value = instance['value']
        date = instance['date']
        mode = self.context['mode']
        if mode == 'weekly':
            key = "هفته ی {} سال {}".format(key, date.year)
        if mode == 'monthly':
            month_number = date.month
            month_name = calendar.month_abbr[month_number]
            year = date.year
            key = "{} {}".format(month_name, year)
        if mode == 'daily':
            key = date.strftime("%d/%m/%Y")

        return {
            'key': key,
            'value': value
        }


class CachedTransactionSerializer(DocumentSerializer):
    class Meta:
        model = CachedTransaction
        fields = '__all__'

    def create(self, validated_data):
        mode = self.context['mode']
        merchant_id = self.context['merchant_id']
        type = self.context['type']

        if merchant_id is not None:
            cached_transaction = CachedTransaction.objects.create(key=validated_data.get('key'),
                                                                  value=validated_data.get('value'),
                                                                  type=type,
                                                                  mode=mode,
                                                                  merchant_id=merchant_id)
        else:
            cached_transaction = CachedTransaction.objects.create(key=validated_data.get('key'),
                                                                  value=validated_data.get('value'),
                                                                  type=type,
                                                                  mode=mode)
        cached_transaction.save()

    def to_representation(self, instance):
        value = instance['value']
        key = instance['key']

        return {
            'key': key,
            'value': value
        }
