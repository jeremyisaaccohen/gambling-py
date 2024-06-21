import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App: React.FC = () => {
  const [balance, setBalance] = useState<number>(1000);
  const [amount, setAmount] = useState<string>('');
  const [number, setNumber] = useState<string>('');
  const [result, setResult] = useState<string>('');
  const [history, setHistory] = useState<any[]>([]);
  const [showHistory, setShowHistory] = useState<boolean>(false);


  // Fetch the current balance when the component mounts
  useEffect(() => {
    const fetchBalance = async () => {
      try {
        const response = await axios.get('/balance');
        setBalance(response.data.balance);
      } catch (error) {
        console.error('Error fetching balance:', error);
      }
    };

    fetchBalance();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get('/history');
      setHistory(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleBet = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await axios.post('/bet', {
        amount: parseInt(amount),
        number: parseInt(number),
      });
      const data = response.data;
      console.log(data);  // Debugging line
      setBalance(data.balance);
      setResult(`Result: ${data.result}, Outcome: ${data.outcome}, Dice Roll: ${data.dice_roll}`);
      if (showHistory) {
        await fetchHistory();
      }
    } catch (error) {
      console.error('Error:', error);
      setResult('Error placing bet. Please ensure sufficient balance! You can always add more :).')
    }
  };

    const handleWithdraw = async () => {
    try {
      const response = await axios.post('/withdraw');
      setBalance(response.data.balance);
      setResult('Balance withdrawn and game reset.');
      if (showHistory) {
        await fetchHistory();
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const toggleHistory = async () => {
    if (showHistory) {
      setShowHistory(false);
      setHistory([]);
    } else {
      try {
        await fetchHistory();
        setShowHistory(true);
      } catch (error) {
        console.error('Error:', error);
      }
    }
  };

  return (
    <div className="App">
      <h1>Welcome to Gomboc Gambling Casino!</h1>
      <p>Current Balance: ${balance}</p>
      <form onSubmit={handleBet}>
        <p>Enter Dice Number (1-6):</p>
        <p>
          <input
            type="number"
            value={number}
            onChange={(e) => setNumber(e.target.value)}
            min="1"
            max="6"
            required
          />
        </p>
        <p>Enter Amount:</p>
        <p>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
        </p>
        <p>
          <input type="submit" value="Submit" />
        </p>
      </form>
      <p>{result}</p>
      <button onClick={toggleHistory}>{showHistory ? 'Hide History' : 'View History'}</button>
      <button onClick={handleWithdraw}>Withdraw</button>

      <ul>
        {history.map(bet => (
          <li key={bet.id}>
            Bet ID: {bet.id}, Amount: {bet.amount}, Number: {bet.number}, Dice Roll: {bet.dice_roll}, Result: {bet.result}, Outcome: {bet.outcome}, Balance: {bet.balance}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
