# Python
import json
from collections import namedtuple
from typing import List

# Web3
from web3.exceptions import ContractLogicError
from web3 import Web3
from web3.datastructures import AttributeDict

# Settings
from settings import (
    PROJECT_ID,
    ABI,
    ADDRESS
)


w3 = Web3(Web3.WebsocketProvider(f'wss://ropsten.infura.io/ws/v3/{PROJECT_ID}'))
abi = json.loads(ABI)
address = w3.toChecksumAddress(ADDRESS)
contract = w3.eth.contract(address=address, abi=ABI)
Owner = namedtuple('Owner', ['address', 'email'])
Transaction = namedtuple('Transaction', ['address', 'amount'])

def get_project_name(id: int) -> str:
    try:
        name = contract.functions.getProjectName(id).call()
    except ContractLogicError as e:
        return
    else:
        return name

def get_project_goal(id: int) -> str:
    try:
        goal = contract.functions.getProjectGoal(id).call()
    except ContractLogicError as e:
        return
    else:
        return format(Web3.fromWei(goal, 'ether'), '.18f')

def get_project_amount(id: int) -> str:
    try:
        goal = contract.functions.getProjectAmount(id).call()
    except ContractLogicError as e:
        return
    else:
        return format(Web3.fromWei(goal, 'ether'), '.18f')

def is_open_project(id: int) -> bool:
    try:
        is_open = contract.functions.getProjectStatus(id).call()
    except ContractLogicError as e:
        return
    else:
        return is_open

def get_project_owner(id: int) -> Owner:
    try:
        owner = contract.functions.getProjectOwner(id).call()
    except ContractLogicError as e:
        return
    else:
        return Owner(*owner)

def create_project(address: str, private_key: str, goal: int, owner_email: str, project_name: str) -> int:
    try:
        transaction = contract.functions.createProject(goal, owner_email, project_name)\
            .buildTransaction({
                'from': address,
                'nonce': w3.eth.getTransactionCount(address),
                'gasPrice': w3.eth.gas_price
            })
        t_signed = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        t_hash = w3.eth.send_raw_transaction(t_signed.rawTransaction)
        tx_receipt = w3.eth.get_transaction_receipt(t_hash)
        event = contract.events.ProjectCreation().processReceipt(tx_receipt)
    except ContractLogicError as e:
        return
    else:
        return event[0].args.id

def fund_project(project_id: int, address: str, private_key: str, amount: int) -> AttributeDict:
    try:
        transaction = contract.functions.fundProject(project_id)\
            .buildTransaction({
                'from': address,
                'value': amount,
                'nonce': w3.eth.getTransactionCount(address),
                'gasPrice': w3.eth.gas_price
            })
        t_signed = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        t_hash = w3.eth.send_raw_transaction(t_signed.rawTransaction)
        tx_receipt = w3.eth.get_transaction_receipt(t_hash)
        event = contract.events.FundingAlert().processReceipt(tx_receipt)
    except ContractLogicError as e:
        return
    else:
        return event[0].args

def get_project_transactions(id: int) -> List[Transaction]:
    try:
        transactions= contract.functions.getProjectTransactions(id).call()
    except ContractLogicError as e:
        return
    else:
        return [Transaction(*t) for t in transactions]

def get_project_contributors(id: int) -> List[Transaction]:
    try:
        contributors = contract.functions.getProjectContributors(id).call()
    except ContractLogicError as e:
        return
    else:
        return [Transaction(*t) for t in contributors]
