from scripts.help_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from web3 import Web3
from brownie import interface,config,network

def main():
    get_weth()

def get_weth():
    """
    Mints WETH by depositing ETH.
    """
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from":account,"value":0.1 * 10**18})
    tx.wait(1)
    print("Received 0.1 WETH")
    return tx