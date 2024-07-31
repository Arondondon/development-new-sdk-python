import web3
from snet.contracts import get_contract_object

from snet.sdk.contract.transaction_handler import get_transaction_handler
from snet.sdk.configs.account import EthAccount


class Contract:
    pass


class EthContract(Contract):
    def __init__(self, w3: web3.Web3, contract_name: str, address: str = None):
        self.w3 = w3
        if address is None:
            self.contract = get_contract_object(self.w3, contract_name)
        else:
            self.contract = get_contract_object(self.w3, contract_name, address)
        self.address = self.contract.address

    def call(self, function_name, *positional_inputs, **named_inputs):
        return getattr(self.contract.functions, function_name)(*positional_inputs, **named_inputs).call()

    def _build_transaction(self, function_name, from_address, nonce, gas_price, *positional_inputs, **named_inputs):
        chain_id = self.w3.net.version
        return getattr(self.contract.functions, function_name)(*positional_inputs, **named_inputs).build_transaction({
            "from": from_address,
            "nonce": nonce,
            "gasPrice": gas_price,
            "chainId": int(chain_id)
        })

    def process_receipt(self, receipt):
        events = []

        contract_events = map(lambda e: e["name"], filter(lambda e: e["type"] == "event", self.abi))
        for contract_event in contract_events:
            events.extend(getattr(self.contract.events, contract_event)().process_receipt(receipt))

        return events

    def _get_gas_price(self):
        gas_price = self.w3.eth.gas_price
        if gas_price <= 15000000000:
            gas_price += gas_price * 1 / 3
        elif 15000000000 < gas_price <= 50000000000:
            gas_price += gas_price * 1 / 5
        elif 50000000000 < gas_price <= 150000000000:
            gas_price += 7000000000
        elif gas_price > 150000000000:
            gas_price += gas_price * 1 / 10
        return int(gas_price)

    def perform_transaction(self, account: EthAccount, function_name, *positional_inputs, **named_inputs):
        gas_price = self._get_gas_price()
        nonce = account.get_nonce(self.w3)
        transaction_handler = get_transaction_handler(account, self.w3)
        address = transaction_handler.get_address()

        transaction = self._build_transaction(function_name, address, nonce, gas_price,
                                              *positional_inputs, **named_inputs)
        receipt = transaction_handler.transact(transaction)

        return receipt

    def call_read_func(self):
        pass

    def call_write_func(self):
        pass

