import ollama
import requests
import json

# Read context file
with open("context.txt", "r", encoding="utf-8") as f:
    context = f.read()

# Ask Ollama to generate BDD scenarios in structured JSON format
prompt = """{context}

Now, please generate **3 BDD scenarios** in **valid JSON format** with this structure:
```json
[
    {{
        "scenario": "Scenario Name",
        "request": {{ "account_id": "user1", "transaction_type": "deposit", "amount": 500 }},
        "expected": {{ "new_balance": 1500 }}
    }}
]
```
for deposit it is using depost as transaction_type and for withdrawl it is using withdraw as transaction_type.

Also initially the bank user has 1000 amount.
Keep in mind never take new balances for each scenario or consider zero or any random balance. 
the same balance(1000) will keep on updating after each and every scenario. 
Also the balance should be indicated as a float value with one decimal places.
You just need to play like a person like deposit 300, withdraw 500 and so on... the inital balance will keep on changing
eg:
1000 = balance
200 deposit, balance becomes 1200.
400 withdraw, becomes 800.
50 deposit, it becomes 850.
Return **only the JSON** output without explanations or extra text.
""".format(context=context)  # Using .format() instead of f-string

# Get BDD scenarios from Ollama
response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

try:
    # Extract response content
    raw_response = response["message"]["content"]
    test_cases = json.loads(raw_response)  # Parse JSON response

    test_results = []

    # Execute each test case
    for test in test_cases:
        scenario_name = test["scenario"]
        request_payload = test["request"]
        expected_response = test["expected"]

        # Send API request
        api_response = requests.post("http://localhost:8000/transaction", json=request_payload)
        actual_response = api_response.json()

        # Compare results
        balance_correct = actual_response.get("new_balance") == expected_response.get("new_balance")
        account_correct = actual_response.get("account_id") == request_payload.get("account_id")

        if balance_correct and account_correct:
            status = "✅ Passed"
        else:
            status = "❌ Failed"

        # Append test result
        test_results.append({
            "scenario": scenario_name,
            "request": request_payload,
            "expected": expected_response,
            "actual": actual_response,
            "status": status
        })

    # Save results to file
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=4)

    print("\n✅ Test execution completed! Check `test_results.json` for results.")

except json.JSONDecodeError:
    print("\n❌ Error: Ollama response is not in JSON format. Check output manually.\n", response)