import web3


def get_address_from_private_key(private_key: str) -> str:
    return web3.Account.from_key(private_key).address


def get_address_and_key_from_mnemonic(mnemonic: str, index: int) -> (str, str):
    web3.Account.enable_unaudited_hdwallet_features()
    account = web3.Account.from_mnemonic(mnemonic, account_path=f"m/44'/60'/0'/0/{index}")
    return account.address, account.key


def normalize_private_key(private_key):
    if private_key.startswith("0x"):
        private_key = bytes(bytearray.fromhex(private_key[2:]))
    else:
        private_key = bytes(bytearray.fromhex(private_key))
    return private_key

