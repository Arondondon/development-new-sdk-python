import abc
import struct
import time

import rlp
import web3
from eth_account.messages import defunct_hash_message
from eth_account._utils.legacy_transactions import encode_transaction, \
    UnsignedTransaction, serializable_unsigned_transaction_from_dict
from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException


from snet.sdk.utils import normalize_private_key
from snet.sdk.configs.account import AccountType, EthAccount

BIP32_HARDEN = 0x80000000


class TransactionHandler(abc.ABC):
    @abc.abstractmethod
    def get_address(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def transact(self, transaction, out_f):
        raise NotImplementedError()

    @abc.abstractmethod
    def sign_message_after_solidity_keccak(self, message):
        raise NotImplementedError()


class KeyOrMnemonicTransactionHandler(TransactionHandler):
    def __init__(self, w3, private_key, address):
        self.w3 = w3
        self.private_key = normalize_private_key(private_key)
        self.address = address

    def get_address(self):
        return self.address

    def transact(self, transaction, out_f):
        raw_transaction = sign_transaction_with_private_key(
            self.w3, self.private_key, transaction)
        return send_and_wait_for_transaction(raw_transaction, self.w3, out_f)

    def sign_message_after_solidity_keccak(self, message):
        return sign_message_with_private_key(self.w3, self.private_key, message)


class LedgerTransactionHandler(TransactionHandler):
    GET_ADDRESS_OP = b"\xe0\x02\x00\x00"
    SIGN_TX_OP = b"\xe0\x04\x00\x00"
    SIGN_TX_OP_CONT = b"\xe0\x04\x80\x00"
    SIGN_MESSAGE_OP = b"\xe0\x08\x00\x00"

    def __init__(self, w3, index):
        self.w3 = w3
        try:
            self.dongle = getDongle(False)
        except CommException:
            raise RuntimeError(
                "Received commException from Ledger. Are you sure your device is plugged in?")
        self.dongle_path = parse_bip32_path("44'/60'/0'/0/{}".format(index))
        apdu = LedgerTransactionHandler.GET_ADDRESS_OP
        apdu += bytearray([len(self.dongle_path) + 1,
                           int(len(self.dongle_path) / 4)]) + self.dongle_path
        try:
            result = self.dongle.exchange(apdu)
        except CommException:
            raise RuntimeError("Received commException from Ledger. Are you sure your device is unlocked and the "
                               "Ethereum app is running?")

        offset = 1 + result[0]
        self.address = self.w3.to_checksum_address(bytes(result[offset + 1: offset + 1 + result[offset]])
                                                   .decode("utf-8"))

    def get_address(self):
        return self.address

    def transact(self, transaction, out_f):
        tx = UnsignedTransaction(
            nonce=transaction["nonce"],
            gasPrice=transaction["gasPrice"],
            gas=transaction["gas"],
            to=bytes(bytearray.fromhex(transaction["to"][2:])),
            value=transaction["value"],
            data=bytes(bytearray.fromhex(transaction["data"][2:]))
        )

        encoded_tx = rlp.encode(tx, UnsignedTransaction)

        overflow = len(self.dongle_path) + 1 + len(encoded_tx) - 255

        if overflow > 0:
            encoded_tx, remaining_tx = encoded_tx[:-overflow], encoded_tx[-overflow:]

        apdu = LedgerTransactionHandler.SIGN_TX_OP
        apdu += bytearray([len(self.dongle_path) + 1 +
                           len(encoded_tx), int(len(self.dongle_path) / 4)])
        apdu += self.dongle_path + encoded_tx
        try:
            print("Sending transaction to Ledger for signature...\n", file=out_f)
            result = self.dongle.exchange(apdu)
            while overflow > 0:
                encoded_tx = remaining_tx
                overflow = len(encoded_tx) - 255

                if overflow > 0:
                    encoded_tx, remaining_tx = encoded_tx[:-overflow], encoded_tx[-overflow:]

                apdu = LedgerTransactionHandler.SIGN_TX_OP_CONT
                apdu += bytearray([len(encoded_tx)])
                apdu += encoded_tx
                result = self.dongle.exchange(apdu)
        except CommException as e:
            if e.sw == 27013:
                raise RuntimeError("Transaction denied from Ledger by user")
            raise RuntimeError(e.message, e.sw)

        transaction.pop("from")
        unsigned_transaction = serializable_unsigned_transaction_from_dict(
            transaction)
        raw_transaction = encode_transaction(unsigned_transaction,
                                             vrs=(result[0],
                                                  int.from_bytes(
                                                      result[1:33], byteorder="big"),
                                                  int.from_bytes(result[33:65], byteorder="big")))
        return send_and_wait_for_transaction(raw_transaction, self.w3, out_f)

    def sign_message_after_solidity_keccak(self, message):
        apdu = LedgerTransactionHandler.SIGN_MESSAGE_OP
        apdu += bytearray([len(self.dongle_path) + 1 +
                           len(message) + 4, int(len(self.dongle_path) / 4)])
        apdu += self.dongle_path + struct.pack(">I", len(message)) + message
        try:
            result = self.dongle.exchange(apdu)
        except CommException:
            raise RuntimeError("Received commException from Ledger. Are you sure your device is unlocked and the "
                               "Ethereum app is running?")

        return result[1:] + result[0:1]


def get_transaction_handler(account: EthAccount, w3: web3.Web3):
    if account.type == AccountType.KEY or account.type == AccountType.MNEMONIC:
        return KeyOrMnemonicTransactionHandler(w3, account.private_key, account.address)
    else:
        return LedgerTransactionHandler(w3, account.index)


def send_and_wait_for_transaction_receipt(txn_hash, w3):
    # Wait for transaction to be mined
    receipt = dict()
    while not receipt:
        time.sleep(1)
        try:
            receipt = w3.eth.get_transaction_receipt(txn_hash)
            if receipt and "blockHash" in receipt and receipt["blockHash"] is None:
                receipt = dict()
        except:
            receipt = dict()
    return receipt


def send_and_wait_for_transaction(raw_transaction, w3, out_f):
    print("Submitting transaction...\n", file=out_f)
    txn_hash = w3.eth.send_raw_transaction(raw_transaction)
    return send_and_wait_for_transaction_receipt(txn_hash, w3)


def parse_bip32_path(path):
    if len(path) == 0:
        return b""
    result = b""
    elements = path.split('/')
    for pathElement in elements:
        element = pathElement.split('\'')
        if len(element) == 1:
            result = result + struct.pack(">I", int(element[0]))
        else:
            result = result + struct.pack(">I", BIP32_HARDEN | int(element[0]))
    return result


def sign_transaction_with_private_key(w3, private_key, transaction):
    return w3.eth.account.sign_transaction(transaction, private_key).rawTransaction


def sign_message_with_private_key(w3, private_key, message):
    h = defunct_hash_message(message)
    return w3.eth.account.signHash(h, private_key).signature

