import hashlib
import time
import uuid

class Block:
    def __init__(self, index, timestamp, sender, receiver, amount, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.transaction_id = str(uuid.uuid4())

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.sender}{self.receiver}{self.amount}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.ctime(), "System", "System", 0, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, sender, receiver, amount):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.ctime(), sender, receiver, amount, latest_block.hash)
        self.chain.append(new_block)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]
            if current.previous_hash != prev.hash:
                return False
            if current.hash != current.calculate_hash():
                return False
        return True

    def get_balance(self, user):
        balance = 0
        for block in self.chain:
            if block.receiver == user:
                balance += block.amount
            if block.sender == user:
                balance -= block.amount
        return balance

    def get_leaderboard(self):
        users = {}
        for block in self.chain:
            if block.receiver not in users:
                users[block.receiver] = 0
            if block.sender not in users:
                users[block.sender] = 0
            users[block.receiver] += block.amount
            users[block.sender] -= block.amount
        users.pop("System", None)
        leaderboard = sorted(users.items(), key=lambda x: x[1], reverse=True)
        return leaderboard
