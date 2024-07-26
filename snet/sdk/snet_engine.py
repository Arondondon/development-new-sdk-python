from snet.sdk.configs.config import Config, BlockchainType
from snet.sdk.configs.account import *
from snet.sdk.contracts.agix_contract import AGIXContract
from snet.sdk.contracts.mpe_contract import MPEContract
from snet.sdk.configs.service import Service

import web3
import json
from typing import Optional


class SNETEngine:
    def __init__(self, config: Config):
        self._config = config
        self.w3 = web3.Web3(web3.HTTPProvider(self._config.eth_rpc_endpoint))

        if self._config.blockchain == BlockchainType.ETHEREUM:
            with open("../snet/sdk/resources/abi/agix_abi.json", "r") as f:
                agix_abi = json.load(f)
            self.agix = AGIXContract(self.w3, self._config.agix_address, agix_abi)
            with open("../snet/sdk/resources/abi/mpe_abi.json", "r") as f2:
                mpe_abi = json.load(f2)
            self.mpe = MPEContract(self.w3, self._config.mpe_address, mpe_abi, self.agix)
            # self.mpe = MPEContract(self.w3, self._config.mpe_address, mpe_abi)

    def create_account(self, name: str, type: str, wallet_address: str, private_key: str = '') -> None:
        if self._config.blockchain == BlockchainType.ETHEREUM:
            self._config.add_account(EthAccount(name, type, wallet_address, private_key))

    def create_service(self, org_id: str, service_id: str, group_name: str) -> None:
        self._config.add_service(Service(org_id, service_id, group_name))

    def get_mpe_wallet_balance(self, account_name: str, wallet_address: str = None) -> Optional[int]:
        if wallet_address is None:
            return self.mpe.balance(self._config.get_account(account_name).wallet_address)
        else:
            return self.mpe.balance(wallet_address)

    def get_agix_balance(self, account_name: str, wallet_address: str = None) -> Optional[int]:
        if wallet_address is None:
            return self.agix.balance_of(self._config.get_account(account_name).wallet_address)
        else:
            return self.agix.balance_of(wallet_address)

    def get_allowance(self, owner_account_name: str, spender_account_name: str,
                      owner_wallet_address: str = None, spender_wallet_address: str = None) -> Optional[int]:

        if owner_wallet_address is None:
            owner_wallet_address = self._config.get_account(owner_account_name).wallet_address
        if spender_wallet_address is None:
            spender_wallet_address = self._config.get_account(spender_account_name).wallet_address

        return self.agix.allowance(owner_wallet_address, spender_wallet_address)

    def transfer_agix(self, sender_account_name: str, recipient_account_name: str, amount: int) -> None:
        self.agix.transfer(self._config.get_account(sender_account_name).wallet_address,
                           self._config.get_account(sender_account_name).private_key,
                           self._config.get_account(recipient_account_name).wallet_address, amount)
