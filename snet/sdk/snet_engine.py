from snet.sdk.configs.config import Config, BlockchainType
from snet.sdk.configs.account import *
from snet.sdk.contract.agix_contract import AGIXContract
from snet.sdk.contract.mpe_contract import MPEContract
from snet.sdk.payment_strategies.default_payment_strategy import DefaultPaymentStrategy
from snet.sdk.service import Service
from snet.sdk.metadata.metadata_provider import IPFSMetadataProvider
from snet.sdk.utils.utils import get_path_to_pb_files

from web3 import Web3
from typing import Optional


class SNETEngine:
    def __init__(self, config: Config):
        self._config = config
        self.w3 = Web3(Web3.HTTPProvider(self._config.eth_rpc_endpoint))

        if self._config.blockchain == BlockchainType.ETHEREUM:
            self.agix = AGIXContract(self.w3, self._config.agix_address)
            self.mpe = MPEContract(self.w3, self._config.mpe_address, self.agix)

        self._services = {}

    def create_account(self, name: str, acc_type: AccountType, private_key_or_mnemonic: str, index: int = None) -> None:
        if self._config.blockchain == BlockchainType.ETHEREUM:
            self._config.add_account(EthAccount(self.w3, name, acc_type, private_key_or_mnemonic, index))

    # TODO: rework it so that it work correctly
    # TODO: get rid of SDKCommand
    # TODO: perhaps, move most of the actions to the Service.__init__
    # TODO: transfer remaining functions ans classes
    def create_service_client(self, org_id: str, service_id: str, group_name=None,
                              payment_channel_management_strategy=None,
                              free_call_auth_token_bin=None,
                              free_call_token_expiry_block=None,
                              options=None,
                              concurrent_calls=1):

        # Create and instance of the Config object, so we can create an instance of SDKCommand
        sdk_config_object = Config(sdk_config=self._sdk_config)
        sdk = SDKCommand(sdk_config_object, args=Arguments(org_id, service_id))

        # Download the proto file and generate stubs if needed
        force_update = self._sdk_config.get('force_update', False)
        if force_update:
            sdk.generate_client_library()
        else:
            path_to_pb_files = self.get_path_to_pb_files(org_id, service_id)
            pb_2_file_name = find_file_by_keyword(path_to_pb_files, keyword="pb2.py")
            pb_2_grpc_file_name = find_file_by_keyword(path_to_pb_files, keyword="pb2_grpc.py")
            if not pb_2_file_name or not pb_2_grpc_file_name:
                sdk.generate_client_library()

        if payment_channel_management_strategy is None:
            payment_channel_management_strategy = DefaultPaymentStrategy(concurrent_calls)

        if options is None:
            options = dict()
        options['free_call_auth_token-bin'] = bytes.fromhex(free_call_auth_token_bin) if \
            free_call_token_expiry_block else ""
        options['free-call-token-expiry-block'] = free_call_token_expiry_block if \
            free_call_token_expiry_block else 0
        options['email'] = self._sdk_config.get("email", "")
        options['concurrency'] = self._sdk_config.get("concurrency", True)

        if self._metadata_provider is None:
            self._metadata_provider = IPFSMetadataProvider(self.ipfs_client, self.registry_contract)

        service_metadata = self._metadata_provider.enhance_service_metadata(org_id, service_id)
        group = self._get_service_group_details(service_metadata, group_name)
        strategy = payment_channel_management_strategy

        service_stub = self.get_service_stub(org_id, service_id)

        pb2_module = self.get_module_by_keyword(org_id, service_id, keyword="pb2.py")

        service_client = ServiceClient(org_id, service_id, service_metadata, group, service_stub, strategy,
                                       options, self.mpe_contract, self.account, self.web3, pb2_module)
        return service_client

    def get_mpe_wallet_balance(self, account_name: str) -> Optional[int]:
        return self.mpe.balance(self._config.get_account(account_name))

    def get_agix_balance(self, account_name: str) -> Optional[int]:
        return self.agix.balance_of(self._config.get_account(account_name))

    def get_allowance(self, owner_account_name: str, spender_addr: str) -> Optional[int]:
        return self.agix.allowance(self._config.get_account(owner_account_name), spender_addr)

    def transfer_agix(self, sender_account_name: str, recipient_account_name: str, amount: int) -> None:
        self.agix.transfer(self._config.get_account(sender_account_name),
                           self._config.get_account(recipient_account_name).address, amount)

