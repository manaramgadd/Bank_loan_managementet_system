// src/components/LoanRequests.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const LoanRequests = ({ token }) => {
  const [loanRequests, setLoanRequests] = useState([]);

  useEffect(() => {
    const fetchLoanRequests = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/loan/request/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setLoanRequests(response.data.loanRequests);
      } catch (err) {
        console.error('Failed to fetch loan requests:', err);
      }
    };

    fetchLoanRequests();
  }, [token]);

  return (
    <div>
      <h2>Loan Requests</h2>
      <ul>
        {loanRequests.map((request) => (
          <li key={request.id}>
            {request.amount} - {request.terms}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LoanRequests;
