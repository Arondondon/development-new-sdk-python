from snet.sdk.contract.contract import *
from snet.sdk.contract.agix_contract import AGIXContract


class MPEContract(EthContract):

    def __init__(self, w3: web3.Web3, address: str = None, agix: AGIXContract = None):
        super().__init__(w3, "MultiPartyEscrow", address)
        self.agix = agix

    def balance(self, account: EthAccount) -> int:
        return self.contract.functions.balances(account.address).call()

    def channels(self, account: EthAccount) -> list:
        return self.contract.functions.channels().call()

    def deposit(self, account: EthAccount, value: int):
        already_approved = self.agix.allowance(account, self.address)

        if already_approved < value:
            self.agix.approve(account, self.address, value)

        return self.perform_transaction(account, "deposit", value)

    def withdraw(self, account: EthAccount, value: int):
        balance = self.balance(account)
        if balance < value:
            raise Exception("Insufficient funds on the MPE balance")
        return self.perform_transaction(account, "withdraw", value)

    def transfer(self, account: EthAccount, recipient: str, value: int):
        return self.perform_transaction(account, "transfer", recipient, value)

    def open_channel(self, account: EthAccount, signer: str, recipient: str,
                     group_id: str, amount: int, expiration: int):
        return self.perform_transaction(account, "openChannel", signer, recipient, group_id, amount, expiration)

    def deposit_and_open_channel(self, account: EthAccount, signer: str, recipient: str,
                                 group_id: str, amount: int, expiration: int):
        return self.perform_transaction(account, "depositAndOpenChannel", signer, recipient,
                                        group_id, amount, expiration)

    def channel_add_funds(self, account: EthAccount, channel_id: int, amount: int):
        return self.perform_transaction(account, "channelAddFunds", channel_id, amount)

    def channel_extend(self, account: EthAccount, channel_id: int, new_expiration: int):
        return self.perform_transaction(account, "channelExtend", channel_id, new_expiration)

    def channel_extend_and_add_funds(self, account: EthAccount, channel_id: int, new_expiration: int, amount: int):
        return self.perform_transaction(account, "channelExtendAndAddFunds", channel_id, new_expiration, amount)

    def channel_claim(self, account: EthAccount, channel_id: int, actual_amount: int,
                      planned_amount: int, actual_gas: int, planned_gas: int):
        return self.perform_transaction(account, "channelClaim", channel_id, actual_amount,
                                        planned_amount, actual_gas, planned_gas)

    def channel_claim_timeout(self, account: EthAccount, channel_id: int):
        return self.perform_transaction(account, "channelClaimTimeout", channel_id)



