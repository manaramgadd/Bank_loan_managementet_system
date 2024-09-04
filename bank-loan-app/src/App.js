
import { jwtDecode } from 'jwt-decode';  // Corrected import statement

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
 // Ensure the correct import
import Home from './pages/Home';
import Login from './pages/Login';
import ProviderDashboard from './pages/ProviderDashboard';
import CustomerDashboard from './pages/CustomerDashboard';
import EmployeeDashboard from './pages/EmployeeDashboard';
import Logout from './components/Logout';  // Import Logout component
import './styles/global.css'; 

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [role, setRole] = useState(null);

  useEffect(() => {
    if (token) {
      try {
        const decodedToken = jwtDecode(token);
        setRole(decodedToken.role);
      } catch (err) {
        console.error("Token decoding error:", err);
        setToken(null);
        setRole(null);
      }
    }
  }, [token]);

  const saveToken = (userToken, userRole) => {
    localStorage.setItem('token', userToken);
    setToken(userToken);
    setRole(userRole);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setRole(null);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login/:role" element={<Login setToken={saveToken} />} />
          <Route
            path="/ProviderDashboard"
            element={token ? <ProviderDashboard token={token} /> : <Navigate to="/" />}
          />
          <Route
            path="/CustomerDashboard"
            element={token ? <CustomerDashboard token={token} /> : <Navigate to="/" />}
          />
          <Route
            path="/EmployeeDashboard"
            element={token ? <EmployeeDashboard token={token} /> : <Navigate to="/" />}
          />
        </Routes>
        {token && <Logout logout={logout} />}
      </div>
    </Router>
  );
}

export default App;
