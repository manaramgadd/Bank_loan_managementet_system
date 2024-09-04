import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import Layout from '../components/Layout/layout';

function Login({ setToken }) {
  const { role } = useParams(); // Role from URL params
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      // Send a request to the Django backend to obtain the token
      const response = await axios.post('http://localhost:8000/api/token/', {
        username,
        password,
      });

      // Assuming the response contains the token and user role
      const { access, role: userRole } = response.data;
      
      // Save the token and role
      setToken(access, userRole);

      // Log the role and navigate to the appropriate dashboard based on role
      console.log('Role from API:', userRole);
      
      if (role === 'provider') {
        navigate('/ProviderDashboard');
      } else if (role === 'customer') {
        navigate('/CustomerDashboard');
      } else if (role === 'employee') {
        navigate('/EmployeeDashboard');
      } else {
        navigate('/'); // Redirect to home if role is not recognized
      }
      
    } catch (err) {
      setError('Login failed. Please check your credentials.');
      console.error('Login error:', err);
    }
  };

  return (
    <Layout>
      <div>
        <h2>Login as {role}</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label>
              Username:
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </label>
          </div>
          <div>
            <label>
              Password:
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </label>
          </div>
          {error && <div style={{ color: 'red' }}>{error}</div>}
          <button type="submit">Login</button>
        </form>
      </div>
    </Layout>
  );
}

export default Login;