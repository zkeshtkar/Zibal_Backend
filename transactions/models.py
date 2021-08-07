from bson import ObjectId
from mongoengine import Document, fields


class Transaction(Document):
    createdAt = fields.DateTimeField()
    amount = fields.LongField(default=0)
    merchantId = fields.ObjectIdField()

    @staticmethod
    def retrieve_all_transactions(type=None, mode=None, merchant_id=None):
        dic = {}
        selected_type = "$amount" if type == "amount" else 1
        if mode == 'daily':
            dic = {
                "$dayOfYear": "$createdAt"
            }
        if mode == 'weekly':
            dic = {
                "$isoWeek": "$createdAt"
            }

        if mode == 'monthly':
            dic = {
                "year": {"$year": "$createdAt"},
                "month": {"$month": "$createdAt"}

            }
        pipeline = [
            {"$group": {"_id": dic, "time": {'$first': '$createdAt'}, "value": {"$sum": selected_type},
                        },
             }, {"$project": {"value": 1, "_id": 0, "date": "$time", "key": "$_id"}}]
        if merchant_id is not None:
            match_dic = {"$match": {"merchantId": ObjectId(merchant_id)}}
            pipeline.insert(0, match_dic)
        transactions = Transaction.objects.aggregate(*pipeline)
        return transactions


class CachedTransaction(Document):
    key = fields.StringField()
    value = fields.LongField(default=0)
    mode = fields.StringField()
    type = fields.StringField()
    merchant_id = fields.ObjectIdField()

    @staticmethod
    def retrieve_all_cached_transactions(type=None, mode=None, merchant_id=None):
        if merchant_id is not None:
            serialized_transactions = CachedTransaction.objects.filter(type=type, mode=mode, merchant_id=merchant_id)
        else:
            serialized_transactions = CachedTransaction.objects.filter(type=type, mode=mode)
        return serialized_transactions
