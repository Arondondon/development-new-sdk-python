from snet.sdk.contracts.contract import *
from snet.sdk.contracts.agix_contract import AGIXContract


class MPEContract(EthContract):

    def __init__(self, w3, address, abi, agix: AGIXContract = None):
        super().__init__(w3, address, abi)
        self.agix = agix

    def balance(self, address: str) -> int: # read contract
        return self.contract.functions.balances(address).call()

    def deposit(self, value: int):
        pass

    def withdraw(self, value: int):
        pass

    def transfer(self, recipient: str, value: int):
        pass

    def channels(self) -> list: # read contract
        return self.contract.functions.channels().call()

    def open_channel(self, signer: str, recipient: str, group_id: str, amount: int, expiration: int):
        pass

    def deposit_and_open_channel(self, signer: str, recipient: str, group_id: str, amount: int, expiration: int):
        pass

    def channel_add_funds(self, channel_id: int, amount: int):
        pass

    def channel_claim(self, channel_id: int, actual_amount: int, planned_amount: int, actual_gas: int, planned_gas: int):
        pass

    def channel_claim_timeout(self, channel_id: int):
        pass

    def channel_extend(self, channel_id: int, new_expiration: int):
        pass

    def channel_extend_and_add_funds(self, channel_id: int, new_expiration: int, amount: int):
        pass







