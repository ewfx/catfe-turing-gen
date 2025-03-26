import React, { useState } from "react";

const TransactionForm = () => {
    const [accountId, setAccountId] = useState("");
    const [transactionType, setTransactionType] = useState("deposit");
    const [amount, setAmount] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Convert amount to float
        const transactionAmount = parseFloat(amount);
        if (isNaN(transactionAmount) || transactionAmount <= 0) {
            alert("Please enter a valid amount greater than zero.");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/transaction/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    account_id: accountId,
                    transaction_type: transactionType,
                    amount: transactionAmount,
                }),
            });

            const data = await response.json();
            console.log("Response:", data);

            if (!response.ok) {
                alert("Transaction failed: " + (data.error || "Unknown error"));
            } else {
                alert(`Transaction successful! Processed ${data.amount} as a ${data.transaction_type}`);
            }
        } catch (error) {
            console.error("Error processing transaction:", error);
            alert("Failed to process transaction. Please try again.");
        }
    };

    return (
        <div>
            <h2>Transaction Form</h2>
            <form onSubmit={handleSubmit}>
                <label>Account ID:</label>
                <input type="text" value={accountId} onChange={(e) => setAccountId(e.target.value)} required />

                <label>Transaction Type:</label>
                <select value={transactionType} onChange={(e) => setTransactionType(e.target.value)}>
                    <option value="deposit">Deposit</option>
                    <option value="withdraw">Withdraw</option>
                </select>

                <label>Amount:</label>
                <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} required />

                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default TransactionForm;
