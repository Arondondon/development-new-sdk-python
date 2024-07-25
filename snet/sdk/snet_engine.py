from snet.sdk.config import Config
from snet.sdk.account import *
from snet.sdk.contracts.mpe_contract import MPEContract
from snet.sdk.service import Service

import web3
import json


class SNETEngine:
    def __init__(self, config: Config):
        self._config = config
        self.w3 = web3.Web3(web3.HTTPProvider(self._config.eth_rpc_endpoint))
        with open("snet/sdk/resources/abi/mpe_abi.json", "r") as f:
            self.abi = json.load(f)
        if self._config.blockchain == 'ethereum':
            self.mpe = MPEContract(self.w3, self._config.mpe_address, self.abi)

    def create_account(self, identity_name: str, identity_type: str, wallet_address: str, private_key: str) -> None:
        if self._config.blockchain == 'ethereum':
            self._config.add_account(EthAccount(identity_name, identity_type, wallet_address, private_key))

    def create_service(self, org_id: str, service_id: str, group_name: str):
        self._config.add_service(Service(org_id, service_id, group_name))

    def get_balance(self, account_name: str, wallet_address: str = None):
        if wallet_address is None:
            return self.mpe.balance(self._config.get_account(account_name).wallet_address)
        else:
            return self.mpe.balance(wallet_address)
