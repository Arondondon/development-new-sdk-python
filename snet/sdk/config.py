from snet.sdk.account import *
from snet.sdk.service import Service


class Config:
    def __init__(self, eth_rpc_endpoint: str, concurrency: bool,
                 network: str, blockchain: str, force_update: bool):
        self.eth_rpc_endpoint = eth_rpc_endpoint
        self.concurrency = concurrency
        self.network = network
        self.blockchain = blockchain
        self.force_update = force_update
        self._accounts = {}
        self._services = {}
        self.mpe_address: str
        self.registry_address: str

    def add_account(self, account: Account) -> None:
        self._accounts.setdefault(account.get_name(), account)

    def add_service(self, service: Service) -> None:
        self._services.setdefault(service.service_id, service)

    def get_account(self, account_name: str) -> Account:
        return self._accounts.get(account_name)

    def get_service(self, service_id: str) -> Service:
        return self._services.get(service_id)

