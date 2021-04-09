class TransactionPool:
    def __init__(self):
      self.transaction_map = {}


    def set_transaction(self, transaction):
      '''
      Set a txn in the txn pool
      '''

      self.transaction_map[transaction.id] = transaction
