import json
import dotenv
from brownie import project, network, accounts, Contract
from fastapi import APIRouter
import os
from web3 import Web3
from brownie.network.account import LocalAccount

dotenv.load_dotenv()
bchain_router = APIRouter(tags=['bchain'])


def get_account() -> LocalAccount:
    account = accounts.add(os.environ.get('PRIVATE_KEY'))
    print(account)
    return account


account = get_account()

p = project.load('brown')
FundMe = p.FundMe
SimpleCollectible = p.SimpleCollectible
network.connect('bsc-testnet')


def get_or_deploy_contract():
    deploy_file_fundme = 'deployed_address_fundme.txt'
    if os.path.exists(deploy_file_fundme):
        with open(deploy_file_fundme, 'r') as f:
            contract_address_fundme = f.read().strip()
        print(f"Loading existing contract for fundme at {contract_address_fundme}")
        contract_address_fundme = Contract.from_abi("Fundme", contract_address_fundme, FundMe.abi)
    else:
        print("Deploying new contract for fundme")
        contract_address_fundme = FundMe.deploy({"from": account, "gas_price": Web3.to_wei("4", "gwei")})
        with open(deploy_file_fundme, 'w') as f:
            f.write(contract_address_fundme.address)

    deploy_file_simple = 'deployed_address_simple.txt'

    if os.path.exists(deploy_file_simple):
        with open(deploy_file_simple, 'r') as f:
            contract_address_simple = f.read().strip()
        print(f"Loading existing contract for simple collectible at {contract_address_simple}")
        contract_address_simple = Contract.from_abi("SimpleCollectible", contract_address_simple, SimpleCollectible.abi)
    else:
        print("Deploying new contract for simple collectible")
        contract_address_simple = SimpleCollectible.deploy({"from": account, "gas_price": Web3.to_wei("4", "gwei")})
        with open(deploy_file_simple, 'w') as f:
            f.write(contract_address_simple.address)

    return contract_address_fundme, contract_address_simple


def payment(to_addr, amount):
    to_addr = Web3.to_checksum_address(to_addr)
    fund_me = FundMe[-1]
    tx = fund_me.fund({"from": account, "value": Web3.to_wei(f"{amount}", "ether")})
    print("Funded")
    balance = fund_me.getUserBalance(account)
    print("Balance: ", balance)
    tx.wait(1)
    tx = fund_me.transferFunds(account, to_addr, Web3.to_wei(f"{amount}", "ether"), {"from": account})
    print("Payment Transfered")


def mint_nft(image_uri):
    simple = SimpleCollectible[-1]
    uri = {
        "name": f"NFT Test for BNB hack",
        "description": f"This is an nft for the BNB hack",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/a6/020_The_lion_king_Snyggve_in_the_Serengeti_National_Park_Photo_by_Giles_Laurent.jpg",
        "file_hash": "blabla",
        "attributes": []
    }
    json_uri = json.dumps(uri)
    tx = simple.createCollectible(image_uri, account, {"from": account, "gas_price": Web3.to_wei("4", "gwei")})
    tx.wait(1)
    print("NFT Minted")
    return simple


fundme, simple = get_or_deploy_contract()
print("Paying")
# payment("0xa4ff6439038Bc7293110a629f09FaE5fB4Ef19Bc", 0.001)
# get_account()
mint_nft(image_uri="")



