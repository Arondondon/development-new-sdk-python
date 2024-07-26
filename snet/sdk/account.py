

class Account:
    def get_name(self) -> str:
        pass


class EthAccount(Account):
    def __init__(self, name: str, acc_type: str, wallet_address: str, private_key: str = ''):
        self.name = name
        self.type = acc_type
        self.wallet_address = wallet_address
        self.private_key = private_key

    def get_name(self) -> str:
        return self.name


class CardanoAccount(Account):
    def __init__(self):
        pass

    def get_name(self):
        pass


