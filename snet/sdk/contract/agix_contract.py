from snet.sdk.contract.contract import *


class AGIXContract(EthContract):
    def __init__(self, w3: web3.Web3, address: str = None):
        super().__init__(w3, "SingularityNetToken", address)

    def balance_of(self, account: EthAccount) -> int:
        return self.contract.functions.balanceOf(account.address).call()

    def allowance(self, account: EthAccount, spender: str) -> int:
        return self.contract.functions.allowance(account.address, spender).call()

    def approve(self, account: EthAccount, spender: str, amount: int):
        return self.perform_transaction(account, "approve", spender, amount)

    def transfer(self, account: EthAccount, recipient: str, amount: int):
        return self.perform_transaction(account, "transfer", recipient, amount)

    def transfer_from(self, account: EthAccount, sender: str, recipient: str, amount: int):
        return self.perform_transaction(account, "transferFrom", sender, recipient, amount)

    def increase_allowance(self, account: EthAccount, spender: str, added_value: int):
        return self.perform_transaction(account, "increaseAllowance", spender, added_value)

    def decrease_allowance(self, account: EthAccount, spender: str, subtracted_value: int):
        return self.perform_transaction(account, "decreaseAllowance", spender, subtracted_value)

