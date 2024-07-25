from snet.sdk.contracts.contract import *

class MPEContract(EthContract):
    #def transfer(self, ):

    def balance(self, address: str):
        return self.contract.functions.balances(address).call()
