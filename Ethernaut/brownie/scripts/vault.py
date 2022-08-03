from web3 import Web3, HTTPProvider


def main():
    w3 = Web3(
        HTTPProvider("https://rinkeby.infura.io/v3/3d1420a94fd74ff5ab560e41dbd6430c")
    )
    print(w3.eth.get_storage_at("0x5476150149D08F4c660c9dd72046e177EbF405E9", 1))
