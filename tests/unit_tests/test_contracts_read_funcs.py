import unittest

from snet.sdk.snet_engine import SNETEngine
from snet.sdk.configs.config import Config, BlockchainType


class TestMPEReadFuncs(unittest.TestCase):

    def setUp(self):
        self.config = Config(eth_rpc_endpoint="https://sepolia.infura.io/v3/2e2c6b9397d04d0f8d2d71b21647aed4",
                             concurrency=False,
                             network="sepolia",
                             blockchain=BlockchainType.ETHEREUM,
                             force_update=False,
                             agix_address="0xf703b9aB8931B6590CFc95183be4fEf278732016",
                             mpe_address="0x7E0aF8988DF45B824b2E0e0A87c6196897744970")
        self.engine = SNETEngine(self.config)
        self.engine.create_account("andrey", "key", "0xe5D1fA424DE4689F9d2687353b75D7a8987900fD",
                                   "YOUR_PRIVATE_KEY")
        self.engine.create_account("kirill", "key", "0x9Fc6bd8e2540db7247A0772aA7eDBFA0A59d78C0")

    def test_get_mpe_balance(self):
        balance = self.engine.get_mpe_wallet_balance("andrey")
        self.assertEqual(balance, 5200000010)

    def test_get_agix_balance(self):
        balance = self.engine.get_agix_balance("andrey")
        self.assertEqual(balance, 989799629572)

    def test_get_allowance(self):
        allowance = self.engine.get_allowance("andrey", "kirill")
        self.assertEqual(allowance, 0)

    def test_transfer_agix(self):
        self.engine.transfer_agix("andrey", "kirill", 10)
        balance = self.engine.get_agix_balance("andrey")
        self.assertEqual(balance, 989799629562)


if __name__ == '__main__':
    unittest.main()
