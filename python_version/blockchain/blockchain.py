"""Implementação do BlockChain """
from threading import Thread, Lock
from block import Block

class BlockChain:
    """BlockChain Class"""

    def __init__(self, difficult=5, max_block_transaction=10):
        self.chain = self.__genesis_block__()
        self.difficult = difficult
        self.max_block_transaction = max_block_transaction

        self.pending_transaction = list()
        self.pending_lock = Lock()

        self.stop_auto_mine = False
        self.mine_lock = Lock()

        self.last_block = self.head_block = self.chain[-1]

        self.start_mine()

    def __genesis_block__(self):
        return [Block("Genesis Block", None)]

    def add_pending_transaction(self, transaction):
        with self.pending_lock:
            self.pending_transaction.append(transaction)

    def mine_pending_transaction(self, transactions):
        """Mine up to 10 transactions at a time"""
        self.last_block = self.chain[-1]
        self.head_block = Block(transactions, self.last_block.hash)
        self.head_block.mine_block(self.difficult)
        self.chain.append(self.head_block)

    def auto_mine(self):
        with self.mine_lock:
            self.stop_auto_mine = False

        while 1:
            if self.stop_auto_mine:
                break

            if len(self.pending_transaction) >= self.max_block_transaction:
                with self.pending_lock:
                    self.mine_pending_transaction(self.pending_transaction[:self.max_block_transaction])
                    del self.pending_transaction[:self.max_block_transaction]


    def start_mine(self):
        self.miner = Thread(target=self.auto_mine, name="Miner", args=[])
        self.miner.setDaemon(True)
        self.miner.start()

    def stop_mine(self):
        with self.mine_lock:
            self.stop_auto_mine = True
            self.miner.join(timeout=5)

    def block_print(self):
        _ = [print(block) for block in self.chain]

# import time
# b = BlockChain()
# count = 1
# timer = time.time()
# while 1:
#     try:
#         if time.time() - timer > 1:
#             timer = time.time()
#             b.add_pending_transaction({"data":count})
#             count += 1
#             print(b.pending_transaction)
#     except KeyboardInterrupt:
#         print("CTRL+C sendend")
#         b.stop_mine()
#         print("OK")
#         b.block_print()
#         break