import unittest

from snet.sdk.snet_engine import SNETEngine
from snet.sdk.config import Config, BlockchainType


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
        self.engine.create_account("andrey", "key", "0xe5D1fA424DE4689F9d2687353b75D7a8987900fD")

    def test_get_mpe_balance(self):
        balance = self.engine.get_mpe_wallet_balance("andrey")
        self.assertEqual(balance, 5200000010)

    def test_get_agix_balance(self):
        balance = self.engine.get_agix_balance("andrey")
        self.assertEqual(balance, 989799629572)


if __name__ == '__main__':
    unittest.main()
