import React from 'react';
import './layout.css'; // Your CSS file for the layout

const Layout = ({ children }) => {
  return (
    <div className="layout">
      <header className="header">
        <h1>Bank Loan App</h1>
        <nav>
          <ul className="nav-links">
            <li><a href="/">Home</a></li>
          </ul>
        </nav>
      </header>

      <main className="main-content">
        {children} {/* This will render the page content */}
      </main>

      <footer className="footer">
        <p>&copy; 2024 Bank Loan Management. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Layout;
