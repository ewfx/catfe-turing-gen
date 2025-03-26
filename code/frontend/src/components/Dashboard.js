import React, { useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const [accountId, setAccountId] = useState("user1");
  const [transactionType, setTransactionType] = useState("deposit");
  const [amount, setAmount] = useState("");
  const [response, setResponse] = useState("");

  const handleTransaction = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/transaction/", {
        account_id: accountId,
        transaction_type: transactionType,
        amount: parseFloat(amount),
      });
      setResponse(JSON.stringify(res.data, null, 2));
    } catch (error) {
      setResponse("Error processing transaction");
    }
  };

  return (
    <div>
      <h2>Financial Dashboard</h2>
      <select onChange={(e) => setTransactionType(e.target.value)}>
        <option value="deposit">Deposit</option>
        <option value="withdraw">Withdraw</option>
      </select>
      <input type="text" placeholder="Amount" onChange={(e) => setAmount(e.target.value)} />
      <button onClick={handleTransaction}>Submit</button>
      <pre>{response}</pre>
    </div>
  );
};

export default Dashboard;
