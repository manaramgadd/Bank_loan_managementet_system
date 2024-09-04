import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Layout from '../components/Layout/layout';

function ProviderDashboard({ token }) {
  const [totalFunds, setTotalFunds] = useState(null);
  const [loans, setLoans] = useState([]);
  const [error, setError] = useState('');
  const [newFundAmount, setNewFundAmount] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchFundAndLoans = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/funds/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setTotalFunds(response.data.fund);
        setLoans(response.data.loans);
      } catch (err) {
        setError('Failed to fetch fund and loan information.');
        console.error('Fetch error:', err);
      }
    };

    if (token) {
      fetchFundAndLoans();
    }
  }, [token]);

  const handleAddFund = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        'http://localhost:8000/api/funds/',
        { total_funds: newFundAmount },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setTotalFunds(response.data);
      setMessage('Fund added successfully!');
      setNewFundAmount('');
    } catch (err) {
      setError('Failed to add fund.');
      console.error('Add fund error:', err);
    }
  };

  if (error) return <div>{error}</div>;

  return (
    <Layout>
      <div>
        <h2>Provider Dashboard</h2>

        {totalFunds ? (
          <div>
            <h3>Fund Details</h3>
            <table border="1" cellPadding="10">
              <thead>
                <tr>
                  <th>Provider</th>
                  <th>Budget</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{totalFunds.lender}</td>
                  <td>${totalFunds.total_funds}</td>
                </tr>
              </tbody>
            </table>
          </div>
        ) : (
          <p>Loading fund details...</p>
        )}

        <h3>Add New Fund</h3>
        <form onSubmit={handleAddFund}>
          <label>
            Amount:
            <input
              type="number"
              step="0.01"
              value={newFundAmount}
              onChange={(e) => setNewFundAmount(e.target.value)}
            />
          </label>
          <button type="submit">Add Fund</button>
        </form>

        {message && <p style={{ color: 'green' }}>{message}</p>}

        <h3>Loans</h3>
        {loans.length > 0 ? (
          <table border="1" cellPadding="10">
            <thead>
              <tr>
                <th>Loan ID</th>
                <th>Deadline</th>
                <th>Interest Rate</th>
                <th>Minimum Payment</th>
                <th>Maximum Payment</th>
              </tr>
            </thead>
            <tbody>
              {loans.map((loan) => (
                <tr key={loan.agreement_id}>
                  <td>{loan.agreement_id}</td>
                  <td>{loan.repayment_deadline}</td>
                  <td>{(loan.interest_rate * 100)}%</td>
                  <td>${loan.min_payment}</td>
                  <td>${loan.max_payment}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No loans available.</p>
        )}
      </div>
    </Layout>
  );
}

export default ProviderDashboard;
