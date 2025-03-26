

import requests
import json
import re

# Read BDD scenario file
BDD_SCENARIO_FILE = "generated_bdd_scenarios.txt"
API_URL = "http://localhost:8000/transaction"

# Load the scenarios
with open(BDD_SCENARIO_FILE, "r", encoding="utf-8") as f:
    bdd_scenarios = f.readlines()

# Initialize results list
test_results = []

# Function to extract scenario details
def parse_scenario(scenario_lines):
    """
    Extracts scenario details (account_id, transaction_type, amount, expected result).
    """
    scenario_data = {"account_id": None, "transaction_type": None, "amount": None, "expected_balance": None, "expected_error": None}

    for line in scenario_lines:
        line = line.strip()

        # Extract account ID
        if 'account ID' in line:
            match = re.search(r'account ID "(.*?)"', line)
            if match:
                scenario_data["account_id"] = match.group(1)

        # Extract transaction type
        if 'transaction_type as' in line:
            match = re.search(r'transaction_type as "(.*?)"', line)
            if match:
                scenario_data["transaction_type"] = match.group(1)

        # Extract amount
        if 'amount as' in line:
            match = re.search(r'amount as (\d+)', line)
            if match:
                scenario_data["amount"] = int(match.group(1))

        # Extract expected balance
        if 'new account balance should be' in line:
            match = re.search(r'new account balance should be (\d+)', line)
            if match:
                scenario_data["expected_balance"] = int(match.group(1))

        # Extract expected error
        if 'should deny the transaction' in line or 'should return an error' in line:
            scenario_data["expected_error"] = "error"

    return scenario_data

# Process each scenario
current_scenario = []
for line in bdd_scenarios:
    if line.strip().startswith("## Scenario:"):
        if current_scenario:
            # Execute previous scenario
            scenario_details = parse_scenario(current_scenario)
            
            if scenario_details["account_id"] and scenario_details["transaction_type"]:
                request_data = {
                    "account_id": scenario_details["account_id"],
                    "transaction_type": scenario_details["transaction_type"],
                    "amount": scenario_details["amount"] if scenario_details["amount"] else 0
                }

                # Send API request
                response = requests.post(API_URL, json=request_data)
                response_data = response.json()

                # Verify response
                test_result = {
                    "scenario": current_scenario[0].strip("## ").strip(),
                    "request": request_data,
                    "response": response_data
                }

                if scenario_details["expected_error"]:
                    if "error" in response_data:
                        test_result["status"] = "✅ Passed"
                    else:
                        test_result["status"] = "❌ Failed"
                else:
                    if "new_balance" in response_data and response_data["new_balance"] == scenario_details["expected_balance"]:
                        test_result["status"] = "✅ Passed"
                    else:
                        test_result["status"] = "❌ Failed"

                test_results.append(test_result)

        # Start new scenario
        current_scenario = [line.strip()]
    else:
        current_scenario.append(line.strip())

# Run last scenario
if current_scenario:
    scenario_details = parse_scenario(current_scenario)
    
    if scenario_details["account_id"] and scenario_details["transaction_type"]:
        request_data = {
            "account_id": scenario_details["account_id"],
            "transaction_type": scenario_details["transaction_type"],
            "amount": scenario_details["amount"] if scenario_details["amount"] else 0
        }

        response = requests.post(API_URL, json=request_data)
        response_data = response.json()

        test_result = {
            "scenario": current_scenario[0].strip("## ").strip(),
            "request": request_data,
            "response": response_data
        }

        if scenario_details["expected_error"]:
            if "error" in response_data:
                test_result["status"] = "✅ Passed"
            else:
                test_result["status"] = "❌ Failed"
        else:
            if "new_balance" in response_data and response_data["new_balance"] == scenario_details["expected_balance"]:
                test_result["status"] = "✅ Passed"
            else:
                test_result["status"] = "❌ Failed"

        test_results.append(test_result)

# Save test results
with open("test_results.json", "w", encoding="utf-8") as f:
    json.dump(test_results, f, indent=4)

print("\n✅ BDD Testing Complete! Results saved in test_results.json ✅\n")
