from brownie import Lottery, accounts, network, config, exceptions
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENV,
    get_account,
    fund_with_link,
    get_contract,
)
from web3 import Web3
import pytest

# current eth price ~1520 => $5 = 0.0033
def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    # entrance fee is $5, ETH is $2,000 => expected fee in ETH  5/2000=0.0025 => 2500000000000000
    expected_entrance_fee = Web3.toWei(0.0025, "ether")
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    assert lottery.lottery_state() == 0
    assert lottery.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery.address)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    STATIC_RNG = 777
    # 777 % 3 = 0
    # Act
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})

    fund_with_link(lottery.address)
    tx = lottery.endLottery({"from": account})
    request_id = tx.events["RequestedRandomness"]["requestId"]
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )

    # Assert
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
