import os
import json
import dotenv
import asyncio  # Import asyncio to run the async main function
from typing import Optional
from web3 import Web3
from brownie import project, network, accounts, Contract
from brownie.network.account import LocalAccount
from brownie.network.contract import ProjectContract
from web3 import Web3

from agents.blockchain_agent.schemas import ContractsData
from globar_vars import Var
web3 = Web3(Web3.HTTPProvider("https://bsc-testnet.infura.io/v3/eab9f2aff8984a57ac11c6043cf87d78"))

# Assuming your DataBase class and ContractsData schema are importable
# from database import DataBase
# from schemas import ContractsData

# --- Environment and Basic Setup ---
dotenv.load_dotenv()


def get_account() -> LocalAccount:
    account = accounts.add(os.environ.get('PRIVATE_KEY'))
    print(account)
    return account


# (The rest of your setup: web3, get_account, project loading, etc.)
# ...

# --- Main Logic: Initialize Contracts from Database ---

async def initialize_contracts_from_db(
        deploying_account: LocalAccount,
        network_name: str
) -> tuple[ProjectContract, ProjectContract]:
    """
    Loads contracts from addresses stored in the database. If not found,
    deploys them and saves the new addresses to the DB.
    """
    print("\n--- Initializing Contracts from Database ---")
    # Instantiate your database class
    deployer_wallet = deploying_account.address

    # 1. Fetch existing contract data from DB
    # We use the deployer's wallet as the unique 'user_id' for this global contract document
    contract_data = await Var.db.get_addresses_from_db(user_id=deployer_wallet)

    needs_db_update = False
    if not contract_data:
        print(f"No contract document found for wallet {deployer_wallet}. Creating a new one.")
        needs_db_update = True
        contract_data = ContractsData(
            user_id=deployer_wallet,
            wallet=deployer_wallet,
            network=network_name
        )

    # 2. Check, Deploy, or Load the FundMe contract
    if contract_data.fund_me:
        print(f"Loading existing FundMe contract from DB address: {contract_data.fund_me}")
        fundme_contract = Contract.from_abi("FundMe", contract_data.fund_me, FundMe.abi)
    else:
        print("Deploying new FundMe contract...")
        fundme_contract = FundMe.deploy({"from": deploying_account})
        contract_data.fund_me = fundme_contract.address
        needs_db_update = True
        print(f"Deployed FundMe to: {fundme_contract.address}")

    # 3. Check, Deploy, or Load the SimpleCollectible contract
    if contract_data.simplecol:
        print(f"Loading existing SimpleCollectible contract from DB address: {contract_data.simplecol}")
        simple_collectible_contract = Contract.from_abi("SimpleCollectible", contract_data.simplecol,
                                                        SimpleCollectible.abi)
    else:
        print("Deploying new SimpleCollectible contract...")
        simple_collectible_contract = SimpleCollectible.deploy({"from": deploying_account})
        contract_data.simplecol = simple_collectible_contract.address
        needs_db_update = True
        print(f"Deployed SimpleCollectible to: {simple_collectible_contract.address}")

    # 4. If any new contracts were deployed, update the database
    if needs_db_update:
        print("Saving updated contract addresses to the database...")
        await Var.db.save_addresses_to_db(contract_data)
        print("Database updated successfully.")

    print("--- Contracts Initialized ---\n")
    return fundme_contract, simple_collectible_contract


def payment(to_addr: str, amount: float) -> str:
    """Sends funds through the FundMe contract."""
    if not fundme or not account:
        return "Error: Contracts are not initialized."
    try:
        to_addr_checksum = Web3.to_checksum_address(to_addr)
        # Fund the contract first
        tx_fund = fundme.fund({"from": account, "value": Web3.to_wei(amount, "ether")})
        tx_fund.wait(1)
        # Transfer from the contract to the destination
        tx_transfer = fundme.transferFunds(account, to_addr_checksum, Web3.to_wei(amount, "ether"), {"from": account})
        tx_transfer.wait(1)
        return f"Payment of {amount} BNB transferred successfully to {to_addr}. Tx: {tx_transfer.txid}"
    except Exception as e:
        return f"Error during payment: {e}"


def get_balance() -> str:
    """Gets the balance of the loaded account from the chain."""
    if not account:
        return "Error: Account is not initialized."
    try:
        balance_wei = web3.eth.get_balance(account.address)
        balance_ether = Web3.from_wei(balance_wei, "ether")
        return f"Account balance for {account.address} is: {balance_ether} BNB"
    except Exception as e:
        return f"Error getting balance: {e}"


def mint_nft(image_url: str) -> str:
    """Mints an NFT with the given image URL."""
    if not simple or not account:
        return "Error: Contracts are not initialized."
    try:
        uri = {
            "name": "BNB Hackathon NFT",
            "description": "An NFT minted via a custom script.",
            "image": image_url,
            "attributes": []
        }
        json_uri = json.dumps(uri)
        tx = simple.createCollectible(json_uri, account, {"from": account})
        tx.wait(1)
        return f"Successfully minted NFT! Transaction hash: {tx.txid}"
    except Exception as e:
        return f"Error minting NFT: {e}"


# --- Running the Async Initialization ---

async def start_blockchain_funcs():
    """Main async function to setup and run the application logic."""
    # Your existing setup logic
    account = get_account()
    network_name = network.show_active()

    # Initialize contracts using the new DB-driven function
    global fundme, simple
    fundme, simple = await initialize_contracts_from_db(account, network_name)

    # You can now call your other functions as normal
    # Example:
    # balance = get_balance()
    # print(balance)

#
p = project.load('agents/blockchain_agent/brown')
network.connect('bsc-testnet')
FundMe = p.FundMe
SimpleCollectible = p.SimpleCollectible
account = get_account()
# # Run the main async function
# asyncio.run(main())
#
# account = get_account()
#     network_name = network.show_active()
#
#     # Initialize contracts using the new DB-driven function
# global fundme, simple
# fundme, simple = await initialize_contracts_from_db(account, network_name)
