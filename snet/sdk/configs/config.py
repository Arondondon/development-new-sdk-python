from snet.sdk.configs.account import *
from snet.sdk.configs.service import Service

from enum import Enum
from typing import Union


class BlockchainType(Enum):
    ETHEREUM = 1
    CARDANO = 2


class Config:
    def __init__(self, eth_rpc_endpoint: str, concurrency: bool,
                 network: str, blockchain: BlockchainType, force_update: bool,
                 mpe_address: str = None, registry_address: str = None, agix_address: str = None):
        self.eth_rpc_endpoint = eth_rpc_endpoint
        self.concurrency = concurrency
        self.network = network
        self.blockchain = blockchain
        self.force_update = force_update
        # self._accounts = Dict[str, Union[Account, CardanoAccount, EthAccount]]
        # self._services = Dict[str, Service]
        self._accounts = {}
        self._services = {}
        self.mpe_address: str = mpe_address if mpe_address else ''
        self.registry_address: str = registry_address if registry_address else ''
        self.agix_address: str = agix_address if agix_address else ''

    def add_account(self, account: Union[Account, CardanoAccount, EthAccount]) -> None:
        self._accounts.setdefault(account.name, account)

    def add_service(self, service: Service) -> None:
        self._services.setdefault(service.service_id, service)

    def get_account(self, account_name: str) -> EthAccount:
        return self._accounts.get(account_name)

    def get_service(self, service_id: str) -> Service:
        return self._services.get(service_id)

