from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest
from scripts.deploy_lottery import deploy_lottery
from brownie import Lottery, accounts, config, network, exceptions


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #Arrage
    lottery = deploy_lottery()
    #Act
    #eth 3200 / 50 $ = 0.019
    expected_entrance_fee = Web3.toWei(0.01,"ether")
    entrance_fee = lottery.getEntranceFee()
    #Assert
    assert entrance_fee == expected_entrance_fee

def test_check_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #Arrage
    lottery = deploy_lottery()
    # Act / asssert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})

def test_can_start_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #Arrage
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    #Act
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})
    #Asser
    assert lottery.players(0) == account