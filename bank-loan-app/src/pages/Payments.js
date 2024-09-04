// Payments.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Payments({ token }) {
  const [payments, setPayments] = useState([]);

  useEffect(() => {
    const fetchPayments = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/loan/payment/', {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
        setPayments(response.data);
      } catch (error) {
        console.error('Failed to fetch payments:', error);
      }
    };

    if (token) {
      fetchPayments();
    }
  }, [token]);

  return (
    <div className="container">
      <h2>Your Payments</h2>
      {payments.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Payment ID</th>
              <th>Loan ID</th>
              <th>Amount</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {payments.map((payment) => (
              <tr key={payment.id}>
                <td>{payment.id}</td>
                <td>{payment.loanId}</td>
                <td>${payment.amount.toFixed(2)}</td>
                <td>{new Date(payment.date).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>You have no payments.</p>
      )}
    </div>
  );
}

export default Payments;
