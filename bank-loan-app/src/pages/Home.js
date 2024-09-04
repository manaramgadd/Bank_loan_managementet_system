// src/pages/Home.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/HomePage.css'
import Logout from '../components/Logout';
import Layout from '../components/Layout/layout';

function Home() {
  const navigate = useNavigate();

  const handleRoleSelection = (role) => {
    navigate(`/login/${role}`);
  };

  return (
    <Layout>
<div className="homepage-container">
      <header className="homepage-header">
        <h1>Welcome to the Bank Loan App</h1>
        <p>Manage your loans efficiently and securely.</p>
      </header>

      <main className="homepage-main">
        <h1>Select Your Role</h1>
      <button onClick={() => handleRoleSelection('provider')}>Login as Provider</button>
      <button onClick={() => handleRoleSelection('customer')}>Login as Customer</button>
      <button onClick={() => handleRoleSelection('employee')}>Login as Employee</button>
      
      </main>
     
      
      <footer className="homepage-footer">
      
    </footer>
  </div>
  </Layout>
  );
}

export default Home;
