from eth_utils import to_bytes
from web3 import Web3, HTTPProvider
from brownie import Privacy
import brownie


def main():
    w3 = Web3(
        HTTPProvider("https://rinkeby.infura.io/v3/3d1420a94fd74ff5ab560e41dbd6430c")
    )
    data = w3.eth.get_storage_at("0x45e5A2cd8f6c5Fb0256fA98A6B7240F8C9DE4E1f", 5)
    print(data)
    print(len(data))
    print(len(b"\xa9\xaa\xf4h\xc5k\xb3\xc9\x18P\x87y\xb4\xcbva"))
    print(data.hex())
    print(type(data.hex()))
    print(b"\xa9\xaa\xf4h\xc5k\xb3\xc9\x18P\x87y\xb4\xcbva".hex())
    print(b"\x00\x00\x00\x00\x01\x01\x01\x01".hex())
    # print(to_bytes("a9aaf468c56bb3c918508779b4cb766142f0d761c43476bd39c981", "bytes16"))
