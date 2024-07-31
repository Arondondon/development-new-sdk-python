from enum import Enum

from snet.sdk.contract.transaction_handler import LedgerTransactionHandler
from snet.sdk.utils import *


class AccountType(Enum):
    KEY = 1
    MNEMONIC = 2
    LEDGER = 3


class Account:
    def get_name(self) -> str:
        pass


class EthAccount(Account):
    def __init__(self, w3: web3.Web3, name: str, acc_type: AccountType,
                 private_key_or_mnemonic: str, index: int = None):
        self.name = name
        self.type = acc_type

        if index is not None:
            self.index = index
        else:
            self.index = 0

        if acc_type == AccountType.KEY:
            self.address = get_address_from_private_key(private_key_or_mnemonic)
            self.private_key = private_key_or_mnemonic
        elif acc_type == AccountType.MNEMONIC:
            self.mnemonic = private_key_or_mnemonic
            self.address, self.private_key = get_address_and_key_from_mnemonic(
                self.mnemonic, self.index
            )
            self.mnemonic = private_key_or_mnemonic
        elif acc_type == AccountType.LEDGER:
            transaction_handler = LedgerTransactionHandler(w3, self.index)
            self.address = transaction_handler.get_address()

        self.nonce = 0

    def get_nonce(self, w3) -> int:
        nonce = w3.eth.get_transaction_count(self.address)
        if self.nonce >= nonce:
            nonce = self.nonce + 1
        self.nonce = nonce
        return nonce


class CardanoAccount(Account):
    def __init__(self):
        pass

    def get_name(self):
        pass


