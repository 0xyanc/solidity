from brownie import accounts, SimpleStorage, config


def read_contract():
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())


def main():
    read_contract()
