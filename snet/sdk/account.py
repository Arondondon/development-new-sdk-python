

class Account:
    def get_name(self) -> str:
        pass


class EthAccount(Account):
    def __init__(self, identity_name: str, identity_type: str, wallet_address: str, private_key: str):
        self.identity_name = identity_name
        self.identity_type = identity_type
        self.wallet_address = wallet_address
        self.private_key = private_key

    def get_name(self) -> str:
        return self.identity_name


class CardanoAccount(Account):
    def __init__(self):
        pass

    def get_name(self):
        pass


