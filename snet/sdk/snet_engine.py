from snet.sdk.configs.config import Config, BlockchainType
from snet.sdk.configs.account import *
from snet.sdk.contract.agix_contract import AGIXContract
from snet.sdk.contract.mpe_contract import MPEContract
from snet.sdk.configs.service import Service

from web3 import Web3
from typing import Optional


class SNETEngine:
    def __init__(self, config: Config):
        self._config = config
        self.w3 = Web3(Web3.HTTPProvider(self._config.eth_rpc_endpoint))

        if self._config.blockchain == BlockchainType.ETHEREUM:
            self.agix = AGIXContract(self.w3, self._config.agix_address)
            self.mpe = MPEContract(self.w3, self._config.mpe_address, self.agix)

    def create_account(self, name: str, acc_type: AccountType, private_key_or_mnemonic: str, index: int = None) -> None:
        if self._config.blockchain == BlockchainType.ETHEREUM:
            self._config.add_account(EthAccount(self.w3, name, acc_type, private_key_or_mnemonic, index))

    def create_service(self, org_id: str, service_id: str, group_name: str) -> None:
        self._config.add_service(Service(org_id, service_id, group_name))

    def get_mpe_wallet_balance(self, account_name: str, wallet_address: str = None) -> Optional[int]:
        if wallet_address is None:
            return self.mpe.balance(self._config.get_account(account_name).address)
        else:
            return self.mpe.balance(wallet_address)

    def get_agix_balance(self, account_name: str) -> Optional[int]:
        return self.agix.balance_of(self._config.get_account(account_name))

    def get_allowance(self, owner_account_name: str, spender_addr: str) -> Optional[int]:
        return self.agix.allowance(self._config.get_account(owner_account_name), spender_addr)

    def transfer_agix(self, sender_account_name: str, recipient_account_name: str, amount: int) -> None:
        self.agix.transfer(self._config.get_account(sender_account_name).address,
                           self._config.get_account(sender_account_name).private_key,
                           self._config.get_account(recipient_account_name).address, amount)

