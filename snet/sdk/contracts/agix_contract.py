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

    def transfer(self, sender_addr: str, private_key: str, recipient_addr: str, amount: int):
        nonce = self.w3.eth.get_transaction_count(sender_addr)
        chaid_id = self.w3.eth.chain_id

        transfer_func = self.contract.functions.transfer(recipient_addr, amount).build_transaction(
            {"chainId": chaid_id, "from": sender_addr, "nonce": nonce}
        )
        signed_transaction = self.w3.eth.account.sign_transasction(transfer_func, private_key=private_key)

        send_transaction = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        transaction_receipt = self.w3.eth.wait_for_transaction_receipt(send_transaction)
        return transaction_receipt

    def transfer_from(self, sender: str, recipient: str, amount: int):
        pass

    def increase_allowance(self, spender: str, added_value: int):
        pass

    def decrease_allowance(self, spender: str, subtracted_value: int):
        pass
