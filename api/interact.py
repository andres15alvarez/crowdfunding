import json
from logging import info

from web3 import Web3

from settings import (
    PROJECT_ID,
    ABI,
    ADDRESS,
    ACCOUNT_PRIVATE_KEY,
)


w3 = Web3(Web3.WebsocketProvider(f'wss://ropsten.infura.io/ws/v3/{PROJECT_ID}'))
abi = json.loads(ABI)
address = w3.toChecksumAddress(ADDRESS)
contract = w3.eth.contract(address=address, abi=ABI)
amount = contract.functions.getAmount().call()
value = int(input('Amount to funding in wei: '))
try:
    t = contract.functions.fundProject().buildTransaction(
        {'value': value}
    )
except Exception as e:
    print(str(e))
else:
    signed = w3.eth.account.sign_transaction(t, private_key=ACCOUNT_PRIVATE_KEY)
    t_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    tx_receipt = w3.eth.get_transaction_receipt(t_hash)
    contract.events.FundingAlert().processReceipt(tx_receipt)