import requests
import time
from datetime import datetime, timedelta

ETHERSCAN_API_KEY = "YourEtherscanAPIKeyHere"
ETHERSCAN_URL = "https://api.etherscan.io/api"
DAYS_INACTIVE = 365  # РљРѕР»-РІРѕ РґРЅРµР№ РЅРµР°РєС‚РёРІРЅРѕСЃС‚Рё

def get_wallet_tx_history(address):
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_URL, params=params)
    data = response.json()
    if data["status"] != "1":
        return []
    return data["result"]

def was_inactive_then_active(address):
    txs = get_wallet_tx_history(address)
    if not txs:
        return False, None, None

    now = datetime.utcnow()
    inactivity_threshold = now - timedelta(days=DAYS_INACTIVE)

    last_old_tx = None
    first_new_tx = None

    for tx in txs:
        tx_time = datetime.utcfromtimestamp(int(tx["timeStamp"]))
        if tx_time < inactivity_threshold:
            last_old_tx = tx_time
        elif tx_time >= inactivity_threshold:
            first_new_tx = tx_time
            break

    if last_old_tx and first_new_tx:
        return True, last_old_tx, first_new_tx
    return False, None, None

def scan_wallets(addresses):
    print(f"рџ”Ќ Scanning {len(addresses)} addresses...")
    for addr in addresses:
        active, last_old, first_new = was_inactive_then_active(addr)
        if active:
            print(f"вљ пёЏ Revival detected for {addr}")
            print(f"    Last old activity: {last_old}")
            print(f"    First new activity: {first_new}\n")
        else:
            print(f"вњ… No recent revival for {addr}")

if __name__ == "__main__":
    wallets_to_scan = [
        "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
        "0xddbd2b932f07c130f6f491bfa1c7b623e3d2f03c",
        "0x742d35cc6634c0532925a3b844bc454e4438f44e"
    ]
    scan_wallets(wallets_to_scan)
