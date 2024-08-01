import web3
import re
from urllib.parse import urlparse
import os
from pathlib import PurePath
import sys
from pathlib import Path

import snet.sdk as sdk

RESOURCES_PATH = PurePath(os.path.dirname(sdk.__file__)).joinpath("resources")


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


def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def is_valid_endpoint(url):
    """
    Just ensures the url has a scheme (http/https), and a net location (IP or domain name).
    Can make more advanced or do on-network tests if needed, but this is really just to catch obvious errors.
    >>> is_valid_endpoint("https://34.216.72.29:6206")
    True
    >>> is_valid_endpoint("blahblah")
    False
    >>> is_valid_endpoint("blah://34.216.72.29")
    False
    >>> is_valid_endpoint("http://34.216.72.29:%%%")
    False
    >>> is_valid_endpoint("http://192.168.0.2:9999")
    True
    """
    try:
        result = urlparse(url)
        if result.port:
            _port = int(result.port)
        return (
                all([result.scheme, result.netloc]) and
                result.scheme in ['http', 'https']
        )
    except ValueError:
        return False


def find_file_by_keyword(directory, keyword):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if keyword in file:
                return file


def get_path_to_pb_files(org_id: str, service_id: str) -> str:
    client_libraries_base_dir_path = Path("~").expanduser().joinpath(".snet")
    path_to_pb_files = f"{client_libraries_base_dir_path}/{org_id}/{service_id}/python/"
    return path_to_pb_files


class add_to_path:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            sys.path.remove(self.path)
        except ValueError:
            pass
