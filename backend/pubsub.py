import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-bbdf2f2a-842b-11eb-99bb-ce4b510ebf19'
pnconfig.publish_key = 'pub-c-7dc20958-9268-459e-9d9e-25d2775f710e'


CHANNELS = {
  'TEST': 'TEST',
  'BLOCK': 'BLOCK',
  'TRANSACTION': 'TRANSACTION'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
              self.blockchain.replace_chain(potential_chain)
              print('\n -- Successfully replaced the local chain')
            except Exception as e:
              print(f'\n -- Did not replace chain {e}')
        elif message_object.channel == CHANNELS['TRANSACTION']:
          transaction = Transaction.from_json(message_object.message)
          self.transaction_pool.set_transaction(transaction)
          print('\n -- Set the new transaction in the transaction pool')


class PubSub():
  """
  Handles the publish/subscriber layer of the application.
  Provides communication between the nodes of the blockchain network.
  """
  def __init__(self, blockchain, transaction_pool):
      self.pubnub = PubNub(pnconfig)
      self.pubnub.subscribe().channels(CHANNELS.values()).execute()
      self.pubnub.add_listener(Listener(blockchain, transaction_pool))

  def publish(self, channel, message):
    """
    Publish the message object to the channel.
    """
    self.pubnub.publish().channel(channel).message(message).sync()

  def broadcast_block(self, block):
    """
    Broadcast a block object to all nodes.
    """
    self.publish(CHANNELS['BLOCK'], block.to_json())

  def broadcast_transaction(self, transaction):
    """
    Broadcast a txn to all ndoes.
    """
    self.publish(CHANNELS['TRANSACTION'], transaction.to_json())


def main():
  pubnub = PubSub()
  time.sleep(1)

  pubnub.publish(CHANNELS['TEST'], {'foo': 'bar'})


if __name__ == '__main__':
  main()
