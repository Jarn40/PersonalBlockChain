"""Protótipo de bloco do blockChain"""
import time
import hashlib
import json

class Block:
    """Block Class"""

    def __init__(self, transaction, lastBlockHash):
        self.timestamp = time.time()
        self.transaction = transaction
        self.last_block_hash = lastBlockHash
        self.nonce = 0
        self.hash = self.generate_block_hash()


    def generate_block_hash(self):
        """Block Hash Generator"""
        return hashlib.sha256(bytes(f'{self.timestamp}{self.transaction}{self.last_block_hash}{self.nonce}', 'utf8')).hexdigest()


    def mine_block(self, difficult):
        """Block Mining"""
        while 1:
            self.hash = self.generate_block_hash()
            if self.hash[:int(difficult)] == '0'*difficult:
                break
            self.nonce += 1

    def __str__(self):
        return json.dumps({
            "timestamp":self.timestamp,
            "transaction": self.transaction,
            "hash": self.hash,
            "last_block_hash": self.last_block_hash
        }, indent=4)
