from unicodedata import decimal
from brownie import accounts, network ,config, LinkToken ,VRFCoordinatorMock, MockV3Aggregator, Contract

FORKED_LOCAL_ENVIRONMENT = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENT
    ):
        return accounts[0]
    
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {"eth_usd_price_feed":MockV3Aggregator,
"vrf_coordinator": VRFCoordinatorMock,
"link_token": LinkToken }

def get_contract(contract_name):
    """"This function will grab contract address from brownie config 
    if defines, otherwie it will deploy a mock version of that ontract,
    and return that mock contract
    Args: 
        contrat_name(string)
    """
    contract_type = contract_to_mock[contract_name]
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]

    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract

DECIMALS = 8 
INITIAL_VALUE = 2_0000_0000_000

def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account=get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from":account})
    link_token = LinkToken.deploy({"from":account})
    VRFCoordinatorMock.deploy(link_token.address, {"from":account})
    print("Deployed!")

def fund_with_link(contract_address, account=None, link_token=None, amount=10000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund contract!")
    return tx
