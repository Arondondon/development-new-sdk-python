from snet.sdk.contracts.contract import EthContract


class AGIXContract(EthContract):
    def __init__(self, w3, address, abi):
        super().__init__(w3, address, abi)

    def balance_of(self, address: str) -> int:
        return self.contract.functions.balanceOf(address).call()

    def allowance(self, owner: str, spender: str) -> int:
        return self.contract.functions.allowance(owner, spender).call()

    def approve(self, spender: str, amount: int):
        pass

    def transfer(self, recipient: str, amount: int):
        pass

    def transfer_from(self, sender: str, recipient: str, amount: int):
        pass

    def increase_allowance(self, spender: str, added_value: int):
        pass

    def decrease_allowance(self, spender: str, subtracted_value: int):
        pass
