import requests
import json
from datetime import datetime
import time


# Solana API endpoint
endpoint = "https://api.mainnet-beta.solana.com"

# JSON-RPC request payload to get validator vote accounts
payload = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getVoteAccounts"
})

# Send the request to the Solana RPC
response = requests.post(endpoint, headers={"Content-Type": "application/json"}, data=payload)

# Parse the response
result = response.json()
validators = result['result']['current']

# Get the total number of validators
validator_count = len(validators)
print(f"Validator Count: {validator_count}")


# Function to get block time details for each slot
def get_block_time(slot):
    endpoint = "https://api.mainnet-beta.solana.com"
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlockTime",
        "params": [slot]
    })

    response = requests.post(endpoint, headers={"Content-Type": "application/json"}, data=payload)
    response_data = response.json()

    # Check if there's an error (e.g., skipped slot)
    if "error" in response_data:
        #print(f"Error fetching block time for slot {slot}: {response_data['error']}")
        return None

    return response_data.get("result")

# Function to get exactly 25 valid block times, skipping over skipped slots
def get_valid_blocks(start_slot, num_blocks_needed=25):
    valid_blocks = []
    current_slot = start_slot

    while len(valid_blocks) < num_blocks_needed:
        block_time = get_block_time(current_slot)
        
        if block_time:
            valid_blocks.append({
                'slot': current_slot,
                'time': block_time
            })
            readable_time = datetime.utcfromtimestamp(block_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Valid Block Slot: {current_slot}, Timestamp: {readable_time}")
        else:
            print(f"Slot {current_slot} skipped, moving to next slot.")
        
        # Move to the next slot
        current_slot += 1
        # Add a delay to avoid hitting the rate limit
        time.sleep(1)

    return valid_blocks

# Starting slot from a recent epoch
recent_start_slot = 280000000  # Replace with a recent valid start slot

# Get 25 valid blocks starting from the recent slot
valid_blocks = get_valid_blocks(recent_start_slot, 25)

# Retrieve timestamps and calculate average block time
block_times = [block['time'] for block in valid_blocks]

# Compute average block time
if len(block_times) > 1:
    total_block_time = 0
    valid_time_intervals = 0

    for i in range(1, len(block_times)):
        time_diff = block_times[i] - block_times[i - 1]
        # Ignore time differences of 0 seconds (duplicate timestamps)
        if time_diff > 0:
            total_block_time += time_diff
            valid_time_intervals += 1

    if valid_time_intervals > 0:
        average_block_time = total_block_time / valid_time_intervals
        print(f"Average Block Time for Recent Epoch: {average_block_time} seconds")
    else:
        print("No valid time intervals to calculate the average block time.")
else:
    print("Not enough blocks to calculate average block time.")


# Starting slot from an epoch in 2022 (approximate start slot from January 2022)
epoch_2022_start_slot = 150000000  # Replace with the correct start slot from 2022

# Get 25 valid blocks starting from the 2022 slot
valid_blocks_2022 = get_valid_blocks(epoch_2022_start_slot, 25)

# Retrieve timestamps and calculate average block time for 2022
block_times_2022 = [block['time'] for block in valid_blocks_2022]

# Compute average block time for 2022
if len(block_times_2022) > 1:
    total_block_time = 0
    valid_time_intervals = 0

    for i in range(1, len(block_times_2022)):
        time_diff = block_times_2022[i] - block_times_2022[i - 1]
        if time_diff > 0:
            total_block_time += time_diff
            valid_time_intervals += 1

    if valid_time_intervals > 0:
        average_block_time_2022 = total_block_time / valid_time_intervals
        print(f"Average Block Time for Epoch in 2022 start slot no. 150000000 : {average_block_time_2022} seconds")
    else:
        print("No valid time intervals to calculate the average block time.")
else:
    print("Not enough blocks to calculate average block time.")
