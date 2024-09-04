import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Layout from '../components/Layout/layout';

function EmployeeDashboard({ token }) {
  const [loanRequests, setLoanRequests] = useState([]);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    agreement_id: '',
    interest_rate: '',
    repayment_deadline: '',
    lender: '',
    min_payment: '',
    max_payment: ''
  });
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    const fetchLoanRequests = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/loan-approves/', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setLoanRequests(response.data);
      } catch (err) {
        setError('Failed to fetch loan requests.');
        console.error('Fetch error:', err.response ? err.response.data : err);
      }
    };

    if (token) {
      fetchLoanRequests();
    }
  }, [token]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleApproveLoan = async (e) => {
    e.preventDefault();
    setError(''); // Clear any previous errors
    setSuccessMessage(''); // Clear any previous success messages

    try {
      const response = await axios.post(
        'http://localhost:8000/api/loan-approves/',
        {
          agreement_id: formData.agreement_id,
          interest_rate: parseFloat(formData.interest_rate),
          repayment_deadline: formData.repayment_deadline,
          lender: formData.lender,
          min_payment: parseFloat(formData.min_payment),
          max_payment: parseFloat(formData.max_payment)
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setSuccessMessage('Loan approved successfully!');
      setFormData({
        agreement_id: '',
        interest_rate: '',
        repayment_deadline: '',
        lender: '',
        min_payment: '',
        max_payment: ''
      });
      setLoanRequests(loanRequests.filter(request => request.application_id !== formData.agreement_id));
    } catch (err) {
      if (err.response && err.response.data) {
        // Display specific error from the server
        const serverError = err.response.data.error || 'Failed to approve loan.';
        setError(`Error: ${serverError}`);
      } else {
        // General error message
        setError('An unexpected error occurred. Please try again later.');
      }
      console.error('Approval error:', err.response ? err.response.data : err);
    }
  };

  return (
    <Layout>
    <div>
      <h2>Employee Dashboard</h2>
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      <h3>Pending Loan Requests</h3>
      {loanRequests.length > 0 ? (
        <table border="1" cellPadding="10">
          <thead>
            <tr>
              <th>Request ID</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loanRequests.map((request) => (
              <tr key={request.application_id}>
                <td>{request.application_id}</td>
                <td>${request.loan_amount}</td>
                <td>{request.approved ? 'Approved' : 'Pending'}</td>
                <td>
                  {!request.approved && (
                    <button onClick={() => setFormData({
                      ...formData,
                      agreement_id: request.application_id
                    })}>
                      Approve Loan
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No loan requests found.</p>
      )}

      {formData.agreement_id && (
        <div>
          <h3>Approve Loan</h3>
          <form onSubmit={handleApproveLoan}>
            <div>
              <label>
                Interest Rate:
                <input
                  type="number"
                  name="interest_rate"
                  value={formData.interest_rate}
                  onChange={handleInputChange}
                  step="0.01"
                  min="0"
                  max="1"
                  required
                />
              </label>
            </div>
            <div>
              <label>
                Deadline:
                <input
                  type="date"
                  name="repayment_deadline"
                  value={formData.repayment_deadline}
                  onChange={handleInputChange}
                  required
                />
              </label>
            </div>
            <div>
              <label>
                Lender ID:
                <input
                  type="text"
                  name="lender"
                  value={formData.lender}
                  onChange={handleInputChange}
                  required
                />
              </label>
            </div>
            <div>
              <label>
                Minimum Payment:
                <input
                  type="number"
                  name="min_payment"
                  value={formData.min_payment}
                  onChange={handleInputChange}
                  step="0.01"
                  required
                />
              </label>
            </div>
            <div>
              <label>
                Maximum Payment:
                <input
                  type="number"
                  name="max_payment"
                  value={formData.max_payment}
                  onChange={handleInputChange}
                  step="0.01"
                  required
                />
              </label>
            </div>
            <button type="submit">Submit</button>
          </form>
        </div>
      )}
   
    </div>
    </Layout>
  );
}

export default EmployeeDashboard;
