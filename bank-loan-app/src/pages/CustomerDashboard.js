import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Layout from '../components/Layout/layout';

function CustomerDashboard({ token }) {
  const [loan_amount, setAmount] = useState('');
  const [terms_conditions, setTerms] = useState('');
  const [loanRequests, setLoanRequests] = useState([]);
  const [approvedLoans, setApprovedLoans] = useState([]);
  const [payment_amount, setPaymentAmount] = useState('');
  const [selectedLoanId, setSelectedLoanId] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [payments, setPayments] = useState([]);
  const [showPayments, setShowPayments] = useState(false); // New state for toggling payment view

  useEffect(() => {
    const fetchLoanData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/loan-requests/', {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
        setLoanRequests(response.data.loanRequests);
        setApprovedLoans(response.data.loans);
      } catch (error) {
        console.error('Failed to fetch loan data:', error);
      }
    };

    const fetchPayments = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/loan-payments/', {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
        setPayments(response.data); // Assuming the API returns a list of payments
      } catch (error) {
        console.error('Failed to fetch payments:', error);
      }
    };

    if (token) {
      fetchLoanData();
      fetchPayments(); // Fetch payments data
    }
  }, [token]);

  const handleLoanRequestSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post(
        'http://localhost:8000/api/loan-requests/',
        { loan_amount: parseFloat(loan_amount), terms_conditions: terms_conditions },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );
      setSuccessMessage('Loan request submitted successfully!');
      setErrorMessage('');
      setAmount('');
      setTerms('');
      setLoanRequests([...loanRequests, response.data]);
    } catch (error) {
      setErrorMessage(error.response.data.error || 'Failed to submit loan request');
      setSuccessMessage('');
    }
  };

  const handlePaymentSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post(
        'http://localhost:8000/api/loan-payments/',
        { loan: selectedLoanId, payment_amount: parseFloat(payment_amount) },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );
      setSuccessMessage('Payment submitted successfully!');
      setErrorMessage('');
      setPaymentAmount('');
      setSelectedLoanId('');
      setPayments([...payments, response.data]); // Update payments after successful payment
    } catch (error) {
      setErrorMessage(error.response.data.error || 'Failed to submit payment');
      setSuccessMessage('');
    }
  };

  return (
    <Layout>
      <div className="container">
        <h2>Customer Dashboard</h2>

        {/* Loan Request Form */}
        <h3>Request a Loan</h3>
        <form onSubmit={handleLoanRequestSubmit}>
          <div>
            <label>
              Loan Amount:
              <input
                type="number"
                value={loan_amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </label>
          </div>
          <div>
            <label>
              Loan Terms:
              <textarea
                value={terms_conditions}
                onChange={(e) => setTerms(e.target.value)}
                required
              />
            </label>
          </div>
          {successMessage && <div className="success-message">{successMessage}</div>}
          {errorMessage && <div className="error-message">{errorMessage}</div>}
          <button type="submit">Submit Loan Request</button>
        </form>

        {/* Display Loan Requests */}
        <h3>Your Loan Requests</h3>
        {loanRequests.length > 0 ? (
          <ul>
            {loanRequests.map((loanRequest) => (
              <li key={loanRequest.application_id}>
                <p>Amount: ${loanRequest.loan_amount}</p>
                <p>Terms: {loanRequest.terms_conditions}</p>
                <p>Status: {loanRequest.approved ? 'Approved' : 'Pending'}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>You have no loan requests.</p>
        )}

        {/* Display Approved Loans and Payment Form */}
        <h3>Your Approved Loans</h3>
        {approvedLoans.length > 0 ? (
          <div>
            <ul>
              {approvedLoans.map((loan) => (
                <li key={loan.agreement_id}>
                  <p>Loan ID: {loan.agreement_id}</p>
                  <p>Loan Amount: ${loan.loan_amount}</p>
                  <p>Interest Rate: {loan.interest_rate * 100}%</p>
                  <p>Repayment Deadline: {loan.repayment_deadline}</p>
                  <button onClick={() => setSelectedLoanId(loan.agreement_id)}>
                    Make a Payment
                  </button>
                </li>
              ))}
            </ul>

            {selectedLoanId && (
              <div>
                <h4>Submit Payment</h4>
                <form onSubmit={handlePaymentSubmit}>
                  <div>
                    <label>
                      Payment Amount:
                      <input
                        type="number"
                        value={payment_amount}
                        onChange={(e) => setPaymentAmount(e.target.value)}
                        required
                      />
                    </label>
                  </div>
                  <button type="submit">Submit Payment</button>
                </form>
              </div>
            )}
          </div>
        ) : (
          <p>You have no approved loans.</p>
        )}

        {/* Payment History Button */}
        <button onClick={() => setShowPayments(!showPayments)}>
          {showPayments ? 'Hide Payments' : 'View Payment History'}
        </button>

        {/* Payment History */}
        {showPayments && payments.length > 0 ? (
          <div>
            <h3>Your Payment History</h3>
            <ul>
              {payments.map((payment) => (
                <li key={payment.id}>
                  <p>Loan ID: {payment.loan}</p>
                  <p>Payment Amount: ${payment.payment_amount}</p>
                  <p>Date: {payment.payment_date}</p>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          showPayments && <p>You have no payment history.</p>
        )}
      </div>
    </Layout>
  );
}

export default CustomerDashboard;
