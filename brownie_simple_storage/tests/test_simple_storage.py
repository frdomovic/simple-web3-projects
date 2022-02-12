from cmath import exp
from brownie import SimpleStorage, accounts
import os
print(os.getenv("WEB3_INFURA_PROJECT_ID"))

def test_deploy():
    #Arrage
    account = accounts[0]
    #act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    #assert
    assert starting_value == expected


def test_updating_storage():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    expected = 15
    simple_storage.store(expected, {"from":account})
    assert simple_storage.retrieve() == expected